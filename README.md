# Consultation

###Database Scheme

Please find the DataBase Scheme [here](https://my.vertabelo.com/doc/vLuKE8xoz8fbOAbmOAVgRCoTlYPNOlvd).

###Features

**Doctor**
    
   1. `PUT /api/v0/assign-office` - Assigns the doctor to an office.
   2. `PUT /api/v0/doctors/:id` - Update Doctor
   3. `POST /api/vo/doctors` - Create Doctor
   3. `GET api/v0/doctors/:id/records` - Get records for a doctor
   4. `GET api/v0/doctors/:id/appointments` - Get appointment schedule for the doctor
   
**Client**

   1. `PUT /api/v0/clients/:id` - Update the information a client
   2. `POST /api/v0/clients/:id/records` - Add a new record
   3. `GET /api/v0/clients/:id/records` - Get list of all records
   4. `DELETE /api/v0/clients/:id/records/:id` - Delete a particular record
   5. `POST /api/v0/clients/:id/share-record` - Share record with a new doctor
   6. `POST /api/v0/clients/:id/reviews` - Add a new feedback
   7. `GET /api/v0/clients/:id/reviews` - Get feedback list
   8. `PUT /api/v0/client/:id/reviews/:id` - Update a feedback
  
**Assistant**

   1. `PUT /api/v0/assistants/:id` - Update assistant
   2. `POST /api/v0/assistants/` - Create assistant

**Office**
    
   1. `GET /api/v0/offices/:id/assistants` - Get list of all office assistants
   2. `GET /api/v0/offices/:id/doctors` - Get list of doctors office
   3. `GET /api/v0/offices/:id/insurances` - Get list of all insurances available at office
   4. `GET /api/v0/offices` - Get list of all the offices
   5. `POST /api/v0/offices/:id/appointments` - Schedule a new appointment
   6. `PUT /api/v0/offices/:id/appointments/:id` - Cancel an appointment
   7. `DELETE /api/v0/offices/:id/appointments/:id` - Delete an appointment
   8. `PUT /api/v0/offices/:id/update-doctor-availability` - Update availability of doctor
   9. `PUT /api/v0/offices/:id/insurances/:id/` - Update an insurance


###Steps

   1. `virtualvenv venv`
   2. `source venv/bin/activate`
   3. `pip install -r requirements.txt`
   4. `python manage.py runserver`
   

