# Equipment Reservation System

### Team D9:

David Sprague, Nick Mountain, Jacob Brown, Ayden Franklin

### Overview:

To permit the use of CSXL equipment that will be avaiable in the future, students must be able to veiw availability of equipment and request equipment. Managers and ambassadoors must be able to see requests and accept them and ensure equipment was used properly.

### Key Personas:

##### Sally Student:

Sally student needs to be able to reserve and check out equipment.

##### Amy Ambassador:

Amy ambassador needs to be able to oversee chekouts, returns, and condition of equipment.

### User Stories

#### Sally Student:

As Sally Student, I need to be able to see what equipment is available for me to reserve and checkout available equipment. I also need to sign a liability waiver the first time I checkout equipment.

#### Amy Ambassador

As Amy Ambassador, I need to check to make sure I am giving equipment to the correct students who reserved them, check the equipment out, and check it back in when it is returned. I also need to keep track of how the condition of the equipment changes between checkout and checkin. I need to be able to uniquely identify each piece of equipment and track which students have which pieces of equipment. I also need to see students' checkout histories, to track for a history of late returns and/or disrespect of equipment.

### WireFrame / Mockup

The wireframe for our project is stored in a figma file. To access the wireframe you will need to navigate to the below link and make an account.

https://www.figma.com/file/XbX6hfwGJLQTOl0MLk5SVY/590-Final-Project?type=design&node-id=0%3A1&mode=design&t=AyWmjYFu8xMUW4UA-1

#### Technical Implementation Opportunities and Planning

1. Extend navigation.component.html file to have button for equipment. Depend on user.py in backend to get users. Depend on permission.py in backend to validate that user has correct permissions to perform an action related to checkouts.

2. Equipment widget. Waiver Widget. Checkout complete widget. Equipment checkout requests widget. Checked out equipment widget. Equipment return component. Equipment reservation component for sally student. XL equipment component for amy ambassador.

3. Add a checkout model. Add an equipment model. Change User model to have certain permissions/data associated with checkouts.

4. The application will need to use new API for creating and getting checkout models. This would require GET, POST, and PUSH HTTP methods. We do not forsee needing to modify existing API. We will also need API routes for getting equipment models. This will require a GET HTTP method.

5. There exists multiple concerns regarding security and privacy of data based on a user's role. These are defined as follows:

&nbsp;&nbsp;&nbsp;&nbsp;<ins>Sally Student:</ins> When checking out equipment, Sally student will have access to all available resources. All equipment already checked out or under repair shall be kept private from a student's access. Upon checking out equipment, only Sally Student will be able to access her resource, all other students will not have access to that data.
Sally Student will not have access to oversight of checking in/out equipment, only the ability to request a checkout.\
&nbsp;&nbsp;&nbsp;&nbsp;<ins>Amy Ambassador:</ins> Amy Ambassador must have privilege to check in/out student equipment. She will have access to see a list of all current reservations, as this data is kept private from student roles. Amy Ambassador should have the ability to 'remove' equipment that has been damaged upon return, so write capabilities to the backend database may be necessary. Student's will only have read capabilities. Amy Ambassador will also have permission to 'turn off' students' access to reserve equipment if they are not respectful of the equipment, whether that be through damages, late return, etc.
