import { MDBDataTable } from "mdbreact";
import { getStudents, deleteStudent } from "../services/StudentService";
import React, { useState, useEffect } from "react";

const MDBtable = () => {
    const [students, setStudents] = useState([]);
    const [isUpdated, setIsUpdated] = useState(false);
    const data = {
        columns: [
            {
                label: "ID",
                field: "studentId",
                sort: "asc",
                width: 150,
            },
            {
                label: "First Name",
                field: "firstName",
                sort: "asc",
                width: 270,
            },
            {
                label: "Last Name",
                field: "lastName",
                sort: "asc",
                width: 200,
            },
            {
                label: "Registration No",
                field: "registrationNo",
                sort: "asc",
                width: 100,
            },
            {
                label: "Email",
                field: "email",
                sort: "asc",
                width: 150,
            },
            {
                label: "Course",
                field: "course",
                sort: "asc",
                width: 100,
            },
            // Add more columns as needed
        ],
        rows: students.map((student) => ({
            studentId: student.studentId,
            firstName: student.FirstName,
            lastName: student.LastName,
            registrationNo: student.RegistrationNo,
            email: student.Email,
            course: student.Course,
        })),
    };

    useEffect(() => {
        getStudents().then((data) => {
            setStudents(data);
            setIsUpdated(false);
        });
    }, [isUpdated]);

    return <MDBDataTable striped bordered small data={data} />;
};

export default MDBtable;
