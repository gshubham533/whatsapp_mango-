from datetime import datetime
from logging import exception
from datetime import datetime, timedelta
import requests
import json
import re
from datetime import datetime
import datetime as dt

from chatbot.cashfree import create_cashfree_payment_link

from .models import Orders, Sellers,Products,Peti


version = "v16.0/"
# phoneid = "100496199665373"
phoneid= "173790305822177"
link = "https://graph.facebook.com/"
# token = "EAAfIZB7KFMUsBABv0TVfah3LUihZBBszIlZC7YQTWvJPTqBVIb2r3oCZAZAtfkDwQxH8UWgZBrIkIngZAl4LKPbyEh4CTZA7vHclxBZCZCc8ycdw8m8qlOgWc9JPhZAtrniEizVF8oJDBZBeIjnRXtpk2rGXuT43izTgrZByd8FRmP78RlxOhp6Cmj0c5"
token = "EAANkvcPwc9QBOwrMfYEdsZBMPZBHqiHXQM79dn6piLz27SM5Umr0DiucqLmLtYhicpEW3le2dZC9elsMZBfZAVB8iovVOspn9n8yFMDi2mf53B5MXz01z6SEY2zS9SRb6BuF3CfKZBSH37kYZBZCsVYrO872rteqhO3cUf8xUZAYB9pmZCsnzW4Amob0pbGPKxTI0ZCsQZDZD"


# @csrf_exempt
class chatbot:
    def __init__(self, cont_inst, msg_inst):
        self.cont_inst = cont_inst
        self.msg_inst = msg_inst
        self.phone = cont_inst.wa_id

    def sellerinst(self):
        print("cust_lead_idddddd:", self.cont_inst.cust_lead_id)
        if self.cont_inst.cust_lead_id is not None:
            seller = Sellers.objects.filter(id=int(self.cont_inst.cust_lead_id)).first()
            print("jjsjsjsjs")
            if not seller:
                print(f"No Sellers object found for cust_lead_id: {self.cont_inst.cust_lead_id}")
            return seller
        else:
            print("cust_lead_id is None")
            return None

    
    def match(self):
        print("matchhhhhhhhhhhhhhhhhhh")
        
        # Check for peti flow
        if self.cont_inst.flow in ["home/peti", "online", "payment_option"] and isinstance(self.cont_inst.quantity, int):
            peti = Peti.objects.filter(id=self.cont_inst.ordered_product_id).first()
            if peti:
                print("Peti match:", peti.name, peti.price)
                return str(peti.price)

        # Default: Products flow (Dozen)
        mat = Products.objects.filter(id=self.cont_inst.ordered_product_id).first()
        if not mat:
            return "0"

        price = mat.price
        quantity = self.cont_inst.quantity
        print(mat, price, quantity)

        try:
            new_quant = str(quantity).replace("Dozen", "").strip()
            total = str(price * int(new_quant))
        except Exception as e:
            print("Calculation error:", e)
            total = "0"
        return total

     
    def get_products(self):
        product = Products.objects.filter(seller=self.cont_inst.cust_lead_id)
        product_data = []
        for i in product:
            product_info={
                "id": str(i.id),
                "title":i.product_name,
                "description":"₹"+str(i.price)
            }
            product_data.append(product_info)
        print("lalllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll",product_data)
        return product_data
    
    def get_peti(self):
        peti = Peti.objects.filter(seller=self.cont_inst.cust_lead_id)
        peti_data = []
        for i in peti:
            peti_info={
                "id": str(i.id),
                "title":i.name,
                "description":str(i.price)
            }
            peti_data.append(peti_info)
        print("lalllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll",peti_data)
        return peti_data
    
    def match_products(self,msg_id):
        print("matchhhprodduct")
        product = Products.objects.filter(id=msg_id).first()
        product_id = product.id
        print(product_id,"dddddddddddddddddddddddddddddddddddddddddddd")
        return product_id
    


    def match_peti(self,msg_id):
        print("matchpetiii")
        peti = Peti.objects.filter(id=msg_id).first()
        peti_id = peti.id
        print(peti_id,"dddddddddddddddddddddddddddddddddddddddddddd")
        return peti_id

#To Update Authkey
        
    def create_order(self, product_id, quantity, address, payment_option, name, phone,total):
        product = Products.objects.get(id=product_id)
        order = Orders.objects.create(
            name=name,
            phone=phone,
            product_id=product,
            quantity=quantity,
            address=address,
            payment_option=payment_option,
            comments = total
        )
        return None


    def send_message(self, msg,total="", payment_link=""):
        phone = self.msg_inst.wa_id
        text = self.msg_inst.msg
        name = self.cont_inst.wa_name
        print("nameee",name)
        seller_inst = self.sellerinst()
        print("nameee",seller_inst.seller_name)
        products = self.get_products()
        petis = self.get_peti()
        qr = seller_inst.qr_code
        phone_number = seller_inst.seller_phone
        # total = self.match()  
    

####Payloads#### 
        replies = {
            #ENTRY MENU STARTS HERE#
           'greetings': {"messaging_product": "whatsapp","recipient_type": "individual","to": phone,"type": "interactive","interactive": {"type": "button","body": {"text": "Hello "+name+"\nWelcome to " + seller_inst.seller_name+"🥭""\n\n*Shop for the fresh mangoes from our farms to your doorstep*\n\n *Delivery is expected between 1-2 days* 🚚\n*Kindly check on any of the options below to proceed.*"},"action": {"buttons": [{"type": "reply","reply": {"id": "<ID 1.1>","title": "Place Order"}},{"type": "reply","reply": {"id": "<ID 1.2>","title": "Enquiry"}}]}}},
           'products' : {"messaging_product": "whatsapp","recipient_type": "individual","to": phone,"type": "interactive","interactive": {"type": "list","header": {"type": "text","text": "Mango Categories"},"body": {"text": "Please select the type of mango you would like to purchase\nfrom our wide range of Mangoes. 🥭"},"action": {"button": "Send","sections": [{"title": "Select from options 🥭","rows": products}]}}},
           'options' : {"messaging_product": "whatsapp","recipient_type": "individual","to": phone,"type": "interactive","interactive": {"type": "button","header": {"type": "text","text": "How would you like to shop? 🛒"},"body": {"text": "Choose any one of the option to continue. 😊"},"action": {"buttons": [{"type": "reply","reply": {"id": "<Button 1>","title": "Shop by Dozen"}},{"type": "reply","reply": {"id": "<Button 2>","title": "Shop by Peti"}}]}}},
           'peti' : {"messaging_product": "whatsapp","recipient_type": "individual","to": phone,"type": "interactive","interactive": {"type": "list","header": {"type": "text","text": "Hello "+name},"body": {"text": "Please select the quantity you would like to purchase from below.📦📦"},"action": {"button": "Send","sections": [{"title": "Select from options","rows": petis}]}}},
           'address' : {"messaging_product": "whatsapp","preview_url": False,"recipient_type": "individual","to": phone,"type": "text","text": {"body": "*Enter delivery location so that our mangoes could reach to you*.🥭\n\n*Please enter your Current Address* :📌:\n\n(𝘏𝘰𝘶𝘴𝘦 𝘯𝘰 ,𝘚𝘵𝘳𝘦𝘦𝘵, 𝘓𝘰𝘤𝘢𝘭𝘪𝘵𝘺, 𝘊𝘪𝘵𝘺, 𝘚𝘵𝘢𝘵𝘦)"}},
           'payment_option': {"messaging_product": "whatsapp","recipient_type": "individual","to": phone,"type": "interactive","interactive": {"type": "button","header": {"type": "text","text": "Payment"},"body": {"text": "Choose any one of the payment method 💳"},"action": {"buttons": [{"type": "reply","reply": {"id": "<Button 1>","title": "Pay Online"}},{"type": "reply","reply": {"id": "<Button 2>","title": "Cash on delivery"}}]}}},
           'summery' : {"messaging_product": "whatsapp","preview_url": False,"recipient_type": "individual","to": phone,"type": "text","text": {"body": "This is your order summary😊\n\n*You will receive your mangoes in 2 to 3 days*.😋🥭\n*Name*:"+name+"\nTotal amount:"+total+"\n*address*:"+self.cont_inst.address+"\n*payment method*:"+self.cont_inst.payment_option}},
           'quantity' : {"messaging_product": "whatsapp","recipient_type": "individual","to": phone,"type": "interactive","interactive": {"type": "list","header": {"type": "text","text": "Hello "+name},"body": {"text": "Please select the quantity you would like to purchase from below.📦📦"},"action": {"button": "Send","sections": [{"title": "Select from options","rows": [{"id": "<ID 1.1>","title": "1 Dozen"},{"id": "<ID 1.2>","title": "2 Dozen"},{"id": "<ID 1.3>","title": "3 Dozen"},{"id": "<ID 1.4>","title": "4 Dozen"},{"id": "<ID 1.5>","title": "5 Dozen"},{"id": "<ID 1.6>","title": "6 Dozen"},{"id": "<ID 1.7>","title": "7 Dozen"},{"id": "<ID 1.8>","title": "8 Dozen"},{"id": "<ID 1.9>","title": "9 Dozen"},{"id": "<ID 1.10>","title": "10 Dozen"}]}]}}},
           'qr': {"messaging_product": "whatsapp","recipient_type": "individual","to": phone,"type": "image","image": {"id": qr}},
           'contact' : {"messaging_product": "whatsapp","recipient_type": "individual","to": phone,"type": "interactive","interactive": {"type": "button","body": {"text": "Hello "+name+  "\n*To know more contact us on* "+phone_number+"\n"+seller_inst.seller_name},"action": {"buttons": [{"type": "reply","reply": {"id": "1","title": "Back"}}]}}},
           'payment' : {"messaging_product": "whatsapp","preview_url": False,"recipient_type": "individual","to": phone,"type": "text","text": {"body": "This is your order Payment link\n\n"+payment_link}},



        }
        url = link + version + phoneid + "/messages"
        headers = {
            'Content-Type' : "application/json",
            'Authorization' : "Bearer " + token
        }
        payload = json.dumps(replies[msg])
        response = requests.post(url=url.rstrip(), data=payload, headers=headers, verify=False)
        rs = json.loads(response.text)
        print(rs)

        ################################ CHECK AND SEND ########################

    def check_and_send(self):
        # self.cont_inst.flow = "hoeee"
        # self.cont_inst.save()
        text = self.msg_inst.msg
        print("cont_inst id:", self.cont_inst.id)
        print("check and send")
        print(self.cont_inst.flow)

        msg_inst = self.msg_inst
        seller1 = ("shop",)
        seller2 = ("nikhil",)
        seller_inst = self.sellerinst()
        print(text,"textttttttt")
        msg_type = msg_inst.msg_type
        interactive_id = self.msg_inst.interactive_id

        if text.lower() in seller1:
        
            print("llllll")
            print("cust_lead_id before:", self.cont_inst.cust_lead_id)
            self.cont_inst.cust_lead_id = 1
            self.cont_inst.save()
            print("cust_lead_id after:", self.cont_inst.cust_lead_id)
            self.send_message("greetings")
            self.cont_inst.flow = "home/name"
            self.cont_inst.save()
            print("in greetins")
            
            # self.cont_inst.save()
            return None
        elif text.lower() in seller2:
            print("asdasda")
            print("cust_lead_id before:", self.cont_inst.cust_lead_id)
            self.cont_inst.cust_lead_id = 2
            print("cust_lead_id after:", self.cont_inst.cust_lead_id)
            self.cont_inst.save()
            print("cuslead",self.cont_inst.cust_lead_id)
            self.send_message("greetings")
            print("belowsend")
            self.cont_inst.flow = "home/name"
            self.cont_inst.save()
            print("asdadasd",self.cont_inst.save())
            return None
        # elif text.lower() in seller3:
        #     self.cont_inst.cust_lead_id = 3
        #     self.send_message("greetings")
        #     self.cont_inst.flow = "home/name"                                         
        #     self.cont_inst.save()
        #     return None
        
   ## PLACE A ORDER ##     
        if self.cont_inst.flow == "home/name" and msg_inst.msg_type == "interactive":
            if self.msg_inst.interactive_id == "<ID 1.1>":
                self.cont_inst.flow = "home/order"
                self.send_message('products')
                self.cont_inst.save()
                return None
    
    ## TRACK ORDER ##
        if self.cont_inst.flow == "home/name" and msg_inst.msg_type == "interactive":
            if self.msg_inst.interactive_id == "<ID 1.2>":
                self.cont_inst.flow = "home/enq"
                self.send_message('contact')
                self.cont_inst.save()
                return None

    ## HAVE A QUERY ##
        if self.cont_inst.flow == "home/enq" and msg_inst.msg_type == "interactive":
            print("hereeeeeeeeee")
            if self.msg_inst.interactive_id == "1":
                self.cont_inst.flow = "home/name"
                self.send_message('greetings')
                self.cont_inst.save()
                return None


        if self.cont_inst.flow == "home/order" and msg_inst.msg_type == "interactive":
            print(self.msg_inst.interactive_id)
            prod = self.match_products(self.msg_inst.interactive_id)
            self.cont_inst.ordered_product_id = prod
            print("asdaaaaaaaaaaaaaaaaaaaaa")
            self.cont_inst.flow = "home/options"
            self.send_message('options')
            self.cont_inst.save()
            return None
        

        if self.cont_inst.flow == "home/options" and msg_inst.msg_type == "interactive":
            if self.msg_inst.interactive_id == "<Button 1>":
                self.cont_inst.flow = "home/dozen"
                self.send_message('quantity')
                self.cont_inst.save()
                return None
            if self.msg_inst.interactive_id == "<Button 2>":
                self.cont_inst.flow = "home/peti"
                self.send_message('peti')
                self.cont_inst.save()
                return None
            
        if self.cont_inst.flow == "home/dozen" and msg_inst.msg_type == "interactive":
            if self.msg_inst.interactive_id == "<ID 1.1>":
                self.cont_inst.quantity = text
                self.cont_inst.flow = "home/address"
                self.send_message('address')
                self.cont_inst.save()
                return None
            if self.msg_inst.interactive_id == "<ID 1.2>":
                self.cont_inst.quantity = text
                self.cont_inst.flow = "home/address"
                self.send_message('address')
                self.cont_inst.save()
                return None
            if self.msg_inst.interactive_id == "<ID 1.3>":
                self.cont_inst.quantity = text
                self.cont_inst.flow = "home/address"
                self.send_message('address')
                self.cont_inst.save()
                return None
            if self.msg_inst.interactive_id == "<ID 1.4>":
                self.cont_inst.quantity = text
                self.cont_inst.flow = "home/address"
                self.send_message('address')
                self.cont_inst.save()
                return None
            if self.msg_inst.interactive_id == "<ID 1.5>":
                self.cont_inst.quantity = text
                self.cont_inst.flow = "home/address"
                self.send_message('address')
                self.cont_inst.save()
                return None
            if self.msg_inst.interactive_id == "<ID 1.6>":
                self.cont_inst.quantity = text
                self.cont_inst.flow = "home/address"
                self.send_message('address')
                self.cont_inst.save()
                return None
            if self.msg_inst.interactive_id == "<ID 1.7>":
                self.cont_inst.quantity = text
                self.cont_inst.flow = "home/address"
                self.send_message('address')
                self.cont_inst.save()
                return None
            if self.msg_inst.interactive_id == "<ID 1.8>":
                self.cont_inst.quantity = text
                self.cont_inst.flow = "home/address"
                self.send_message('address')
                self.cont_inst.save()
                return None
            if self.msg_inst.interactive_id == "<ID 1.9>":
                self.cont_inst.quantity = text
                self.cont_inst.flow = "home/address"
                self.send_message('address')
                self.cont_inst.save()
                return None
            if self.msg_inst.interactive_id == "<ID 1.10>":
                self.cont_inst.quantity = text
                self.cont_inst.flow = "home/address"
                self.send_message('address')
                self.cont_inst.save()
                return None
            
        if self.cont_inst.flow == "home/peti" and msg_inst.msg_type == "interactive":
            pett = self.match_peti(self.msg_inst.interactive_id)
            self.cont_inst.quantity = text
            print("asdaaaaaaaaaaaaaaaaaaaaa")
            self.cont_inst.flow = "home/address"
            self.send_message('address')
            self.cont_inst.save()
            return None
        
        if self.cont_inst.flow == "home/address" and msg_inst.msg_type == "text":
            self.cont_inst.address = text
            if seller_inst.cod_status == 1:
                self.send_message("payment_option")
                self.cont_inst.flow = "payment_option"
                self.cont_inst.save()
            else:
                self.cont_inst.flow = "online"
                total= self.match()
                self.create_order(self.cont_inst.ordered_product_id,self.cont_inst.quantity,self.cont_inst.address,self.cont_inst.payment_option,self.cont_inst.wa_name,self.msg_inst.wa_id,total)
                self.send_message("summery",total)
                self.send_message("qr")
                self.cont_inst.save()
            return None
        
        if self.cont_inst.flow == "payment_option" and msg_inst.msg_type == "interactive":
            if self.msg_inst.interactive_id == "<Button 1>":
                self.cont_inst.payment_option = text
                self.cont_inst.flow = "online"
                total = self.match()
                self.create_order(self.cont_inst.ordered_product_id,self.cont_inst.quantity,self.cont_inst.address,self.cont_inst.payment_option,self.cont_inst.wa_name,self.msg_inst.wa_id,total)
                payment_link = create_cashfree_payment_link(
                    order_id=self.cont_inst.id,
                    amount=total,
                    name=self.cont_inst.wa_name,
                    phone=self.msg_inst.wa_id
                )
                print("paymentlink",payment_link)
                if payment_link:
                    self.send_message("summery", total)
                    self.send_message("payment",payment_link=payment_link)
                else:
                    self.send_message("text", "Sorry, payment link generation failed. Please try again.")
                self.cont_inst.save()
                return None
            if self.msg_inst.interactive_id == "<Button 2>":
                self.cont_inst.payment_option = text
                self.cont_inst.flow = "cod"
                total = self.match()
                self.create_order(self.cont_inst.ordered_product_id,self.cont_inst.quantity,self.cont_inst.address,self.cont_inst.payment_option,self.cont_inst.wa_name,self.msg_inst.wa_id,total)
                self.send_message('summery',total)
                # self.send_message("summery",total)

                self.cont_inst.save()
                return None

        