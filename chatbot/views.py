import base64,time
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from chatbot.models import Contacts, Messages
from datetime import datetime
from . mango import chatbot
import os.path


@api_view(['POST','GET'])
def webhook(request):
    if request.method == 'GET':
        chall = request.GET.get("hub.challenge")
        return HttpResponse(chall,status=200)
        # return JsonResponse({"error":"GET method not allowed"})
    if request.method == 'POST':
        print("IN Webhook Post")
        data = request.data["entry"][0]["changes"][0]["value"]
        print(data)
        if "messages" in data:
            contact = data["contacts"][0]
            mess = data["messages"][0]
            wa_id = contact["wa_id"]
            try:
                cont_inst = Contacts.objects.create(
                    wa_id = wa_id,
                    wa_name = contact["profile"]["name"],
                    flow = "home"
                    
                )
            except Exception as e:
                cont_inst = Contacts.objects.get(wa_id = wa_id)
            msg_time = int(mess["timestamp"])
            msg_time = datetime.fromtimestamp(msg_time)
            try:
                if mess["type"] == "text":
                    msg = Messages.objects.create(
                        wa_id = wa_id,
                        msg_id = mess["id"],
                        msg = mess["text"]["body"],
                        timestamp = msg_time,
                        msg_type = mess["type"]
                    )
                elif mess["type"] == "interactive":
                    if "button_reply" in mess["interactive"]:
                        interactive_msg = mess["interactive"]["button_reply"]["title"]
                        interactive_id = mess["interactive"]["button_reply"]["id"]
                    elif "list_reply" in mess["interactive"]:
                        interactive_msg = mess["interactive"]["list_reply"]["title"]
                        interactive_id = mess["interactive"]["list_reply"]["id"]

                    msg = Messages.objects.create(
                        wa_id = wa_id,
                        msg_id = mess["id"],
                        timestamp = msg_time,
                        msg_type = mess["type"],
                        msg = interactive_msg, 
                        interactive_id = interactive_id
                    )

                elif mess["type"] == "button":
                    interactive_id = mess["button"]["payload"]
                    interactive_msg = mess["button"]["text"]

                    msg = Messages.objects.create(
                        wa_id = wa_id,
                        msg_id = mess["id"],
                        timestamp = msg_time,
                        msg_type = mess["type"],
                        msg = interactive_msg, 
                        interactive_id = interactive_id
                    )
              
                elif mess["type"] == "image":
                    media_id = mess["image"]["id"]
                    mime_type = mess["image"]["mime_type"]
                    sha256 = mess["image"]["sha256"]
                    timestamp = mess["timestamp"]

                    msg = Messages.objects.create(
                        msg_id = mess["id"],
                        wa_id = wa_id,
                        timestamp = msg_time,
                        msg_type = mess["type"],
                        msg = "", 
                        interactive_id = "",
                        mime_type = mime_type

                    )
                
                    
            except Exception as e:
                print(e)
            try:       
                ca = chatbot(cont_inst,msg)
                if mess["type"] == "image":
                    url = ca.retrieve_url(media_id)
                    rep = ca.download_media(url)
                    encoded_data = base64.b64encode(rep)
                    ts = int(time.time())
                    mime = mime_type.split("/")[1]
                    file = os.path.join ('static/pancard_images/' + 'image_' + str(ts)+"."+mime)
                    write_file = open(file,"wb")
                    write_file.write(base64.decodebytes(encoded_data))
                    write_file.close()
                    image_path = ('static/pancard_images/' + 'image_' + str(ts)+"."+mime)
                    msg.img_path =image_path
                    msg.save()
                    # Messages.objects.create(
                    #     img_path = image_path
                    # )
                if cont_inst.flow == "home/grt/language/name/biz/pin/pan" and mess["type"] == "image":
                    cont_inst.img_path = image_path
                    cont_inst.save()
                ca.check_and_send()

            except Exception as e:
                print(e)
        return JsonResponse({"success":"Cool"},status=200)