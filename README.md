# Consultation

![Schema](https://github.com/jinxac/consultation/blob/master/schema.png)



### Features


**Auth**

   1. `POST /api/v0/register/`
        
        Signs up a user and based on role assigns the permissions and creates Doctor, Client or Assistant
        object in respective tables. Also creates an admin role to manage the application
        
   2. `POST /api/token/`
   
        Generates JWT token for an active user and returns access token and refresh token
        
   3. `POST /api/token/refresh/`
   
        Refreshes the JWT token based on valid access token
        
**Doctors**

   1. `GET /api/v0/doctors/`
    
        Get the list of doctors. This data is only available to authenticated users. This can be used
        by clients, assistants as well as the other doctors
       
   2. `GET /api/v0/doctors/:id`

        Get the detail view of a doctor. This data is only available to authenticated users. This can be used
        by clients, assistant as well as the other doctors
       
   3. `PUT /api/v0/doctors/:id`
    
        Updates a doctor. The respective doctor can only change his data and not of the other doctors.
   
   4. `POST /api/v0/appointments/get-records/`
   
        Gets the records for an appointment

**Assistants**

   1. `GET /api/v0/assistants/`
    
        Get the list of assistants. This data is only available to admin user and assistant user(For his/her data). In future, 
        this can further be divided and only doctors who manage assistants can view the data.
       
   2. `GET /api/v0/assistants/:id`

        Get the detail view of an assistant. his/her data is only available to authenticated admins and assistant himself/herself.
         In future, this can further be divided and can be accessed by doctors who manage assistants can view the data.
       
   3. `PUT /api/v0/assistants/:id`
    
        Updates an assistant. The respective assistant can only change his data and not of the other assistants.
   
   

**Clients**

   1. `GET /api/v0/clients/`
   
        Gets the list of the clients. This data will only be available to the doctors and the assistants.
        In Future, this can be further divided and restricted to employees(doctor, assistant) of a particular office
        
   2. `GET /api/v0/clients/:id`
   
        Gets the detailed view of the client. The data will be available to client, doctors and assistants. 
        In Future, this can be further divided and restricted to employees(doctor, assistant) of a particular office
  
   3. `PUT /api/v0/clients/:id`
    
        Update the client information. This can be done by client.
       
   4.  `POST /api/v0/clients/add-record`
   
       Adds a record for a booked appointment and uploads the same to aws s3. The data is saved as client-id/appointment-id/doc-id
       
   5. `POST /api/v0/clients/revoke-record`
   
       Revokes the access to the record. The client or the doctor can no longer see the particular record
      
       
   6.  `POST /api/v0/appointments/get-records/`
   
       Gets the records for an appointment
     


**Office**

   1. `GET /api/v0/offices/`
    
        Get the list of offices. This data is available only to authenticated users
       
   2. `GET /api/v0/offices/:id`

        Get the detail view of an office. This data is available only to authenticated users.
       
   3. `PUT /api/v0/offices/:id`
    
        Updates an office. This operation can only be done by Doctors. In future, a super admin can be created
        to do CRUD on office. Only admin user can perform this action
   
   4. `POST /api/v0/offices`
   
        Adds a new office. Only admin user can perform this action
   

**Appointments**

   1. `GET /api/v0/appointments/`
    
        Get the list of appointments. This data is available only to doctors, assistants and clients.
        
   2. `POST /api/v0/appointments/`
   
        Creates an appointment. This operation can only be done by Assistants. This can be extended
        to give the functionality to doctors(or other assistants) too in case the assistant is on leave
        or available.    
       
   2. `GET /api/v0/appointments/:id`

        Get the detail view of an appointment. This data is available only to doctors and assistants.
       
   3. `PUT /api/v0/appointments/:id`
    
        Updates an appointment. This operation can only be done by Assistants. This can be extended
        to give the functionality to doctors(or other assistants) too in case the assistant is on leave
        or available.
   
   4. `POST /api/v0/appointments/:id/records`
   
        Gets the records for an appointment that are not revoked. This data is only available to the doctor.
        
        
**Records**


   1. `GET /api/v0/shared-records`
   
       Gets non revoked shared records for a doctor. This data is only visible to doctors and clients
       
   2. `POST /api/v0/shared-records`
   
       Share a non revoked record with a doctor.
       
 
 
**Feedback**

   1. `GET /api/v0/feedback`
   
       Gets list of feedback. This is visible to authenticated users
       
   2. `POST /api/v0/feedback`
   
       Add a feedback. This action can be performed by clients. This in future can be extended to 
       adding the appointment and sharing feedback on that appointment only
       
   3. `PUT /api/v0/feedback`
   
       Updating the feedback
       
   4. `GET /api/v0/feedback/:id`
   
       Gets list of feedback. This is visible to authenticated users
   
        
### Steps

   1. `virtualvenv venv`
   2. `source venv/bin/activate`
   3. `pip install -r requirements.txt`
   4. `python -m scripts.init_db`
   4. `python manage.py runserver`
 
