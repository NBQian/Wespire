import React, { useState, useEffect } from "react";
import {
    Table,
    Form,
    InputGroup,
    FormControl,
    Pagination,
} from "react-bootstrap";
import { getStudents, deleteStudent } from "../services/StudentService";
import "./Style.css";

const ReactTable = () => {
    const [searchQuery, setSearchQuery] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [students, setStudents] = useState([]);
    const [isUpdated, setIsUpdated] = useState(false);
    const pageSize = 10; // Show 10 students per page
    useEffect(() => {
        getStudents().then((data) => {
            setStudents(data);
            setIsUpdated(false);
        });
    }, [isUpdated]);

    const handleSearch = (event) => {
        setSearchQuery(event.target.value.toLowerCase());
        setCurrentPage(1); // Reset to first page on search
    };

    // Filter students based on search query
    const filteredStudents = students.filter(
        (student) =>
            !searchQuery ||
            student.FirstName.toLowerCase().includes(searchQuery)
    );

    // Calculate pagination details
    const pageCount = Math.ceil(filteredStudents.length / pageSize);
    const pages = Array.from({ length: pageCount }, (_, index) => index + 1);
    const paginatedStudents = filteredStudents.slice(
        (currentPage - 1) * pageSize,
        currentPage * pageSize
    );

    return (
        <div>
            <InputGroup className="mb-3">
                <FormControl
                    placeholder="Search by first name"
                    onChange={handleSearch}
                />
            </InputGroup>

            <Table responsive="md" className="rounded">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Registration No</th>
                        <th>Email</th>
                        <th className="course-column">Course</th>
                        {/* Add more headers as needed */}
                    </tr>
                </thead>
                <tbody>
                    {paginatedStudents.map((student, index) => (
                        <tr key={index}>
                            <td>{student.studentId}</td>
                            <td>{student.FirstName}</td>
                            <td>{student.LastName}</td>
                            <td>{student.RegistrationNo}</td>
                            <td>{student.Email}</td>
                            <td className="course-column">{student.Course}</td>
                            {/* Add more data cells as needed */}
                        </tr>
                    ))}
                </tbody>
            </Table>

            <Pagination className="justify-content-center">
                {pages.map((page) => (
                    <Pagination.Item
                        key={page}
                        active={page === currentPage}
                        onClick={() => setCurrentPage(page)}
                    >
                        {page}
                    </Pagination.Item>
                ))}
            </Pagination>
        </div>
    );
};

export default ReactTable;
