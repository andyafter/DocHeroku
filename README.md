# DocHeroku

This is the back end for the doctor finding app. If you want to run it just follow the right way of running a flask
project. But use **sudo** when run it. 

If you don't have the database file you can always create one yourself.

The API provided so far:
- http://localhost:5000/deleteById/<ID_num>
- http://localhost:5000/queryById/<ID_num>
- http://localhost:5000/update        
- http://localhost:5000/createClinic
- /refreshqueue/\<iden\>
- /queue   [POST]
- /registration  [POST]

The update and createClinic, these two are POST requests and the information you should provide should look like this :
{

  "id" : blabla,
  
  "name": hospital name,
  
  "address1": first line of address,
  
  "address2": second line of address

}

In the newer versio  I will eradicate everything that contains id in the request. Make the id generation an automatic procedure. 

**/refreshqueue** is actually used to refresh all doctors' current queue number as 0. In a word, after one day work, you will want to refresh the queue number, make it 0 for the next day.

**/queue** is a POST request, you send information as a JSON with the key "uuid" and "clinic\_name", you get return with a JSON that contains informatin about "ququq\_num", "key", and "doctor".

**/registration** is also a POST request. You will have to make sure that you pass the name, ic_num and queue_num. 
You can also provide phone_num with it.

