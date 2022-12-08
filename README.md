# Attendance System

- This is an Attendance marking System using `face-recognition` from `open-cv` library.
- This project is in the form of a `flask app`, mainly to be used as an API in an Android project.
- It has features of Registration of a new face, marking attendance of registered faces from an image, also one can view the attendance sheet using the `Show list` button.
- The attendance sheet contains the name of the person, date and time of marking of the attendance in CSV format.
- The `encodings` of each person registered are stored in `student_encodings.csv` and the corresponding names in `student_names.csv`
