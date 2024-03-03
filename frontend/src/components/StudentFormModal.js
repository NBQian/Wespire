import React, { useState, useEffect } from "react";
import { Modal, Row, Form, Button } from "react-bootstrap";
import { addStudent, updateStudent } from "../services/StudentService";
import ReactDatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const StudentFormModal = (props) => {
    const { isUpdate, student, setUpdated, onHide, ...modalProps } = props;
    const [isSubmitted, setIsSubmitted] = useState(false);
    const [formData, setFormData] = useState({
        FirstName: "",
        LastName: "",
        Email: "",
        PhoneNumber: "",
        DateOfBirth: null, // Use null for the initial state of DateOfBirth
    });

    useEffect(() => {
        // Populate formData when the modal is shown and if it's an update operation
        if (props.show && isUpdate && student) {
            setFormData({
                FirstName: student.FirstName || "",
                LastName: student.LastName || "",
                Email: student.Email || "",
                PhoneNumber: student.PhoneNumber || "",
                DateOfBirth: student.DateOfBirth || "",
            });
        } else {
            setIsSubmitted(false);
            // Reset form data when the modal is closed
            setFormData({
                FirstName: "",
                LastName: "",
                Email: "",
                PhoneNumber: "",
                DateOfBirth: null,
            });
        }
    }, [props.show, isUpdate, student]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevState) => ({
            ...prevState,
            [name]: value,
        }));
    };

    const handleDateChange = (date) => {
        setFormData((prevState) => ({
            ...prevState,
            DateOfBirth: date.toISOString().split("T")[0],
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(formData);

        const action = isUpdate
            ? updateStudent(student.studentId, formData)
            : addStudent(formData);

        action.then(
            (result) => {
                setIsSubmitted(true);
                setTimeout(() => {
                    props.setUpdated(true);
                    props.onHide();
                }, 500);
                setUpdated(true);
            },
            (error) => {
                console.log(error.message);
                alert(
                    isUpdate
                        ? "Failed to Update Student"
                        : "Failed to Add Student"
                );
            }
        );
    };

    return (
        <Modal
            {...modalProps}
            aria-labelledby="contained-modal-title-vcenter"
            centered
            onHide={onHide}
        >
            <Modal.Header closeButton>
                <Modal.Title
                    id="contained-modal-title-vcenter"
                    className="centered-modal-title"
                >
                    {isUpdate
                        ? "Update Client Information"
                        : "Add Client Information"}
                </Modal.Title>
            </Modal.Header>

            <Modal.Body>
                <Row>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group controlId="FirstName">
                            <Form.Label>First Name</Form.Label>
                            <Form.Control
                                type="text"
                                name="FirstName"
                                required
                                placeholder=""
                                defaultValue={isUpdate ? student.FirstName : ""}
                                onChange={handleChange}
                            />
                        </Form.Group>
                        <Form.Group controlId="LastName">
                            <Form.Label>Last Name</Form.Label>
                            <Form.Control
                                type="text"
                                name="LastName"
                                required
                                placeholder=""
                                defaultValue={isUpdate ? student.LastName : ""}
                                onChange={handleChange}
                            />
                        </Form.Group>
                        <Form.Group controlId="DateOfBirth">
                            <Form.Label>Date of Birth</Form.Label>
                            <ReactDatePicker
                                selected={formData.DateOfBirth}
                                onChange={handleDateChange}
                                dateFormat="yyyy-MM-dd"
                                className="form-control custom-datepicker"
                                placeholderText="Select date"
                                showYearDropdown
                                yearDropdownItemNumber={40}
                                scrollableYearDropdown
                            />
                        </Form.Group>
                        <Form.Group controlId="Email">
                            <Form.Label>Email</Form.Label>
                            <Form.Control
                                type="text"
                                name="Email"
                                required
                                placeholder=""
                                defaultValue={isUpdate ? student.Email : ""}
                                onChange={handleChange}
                            />
                        </Form.Group>
                        <Form.Group controlId="PhoneNumber">
                            <Form.Label>Phone Number</Form.Label>
                            <Form.Control
                                type="tel"
                                name="PhoneNumber"
                                pattern="[+\d\s().-]+"
                                defaultValue={
                                    isUpdate ? student.PhoneNumber : ""
                                }
                                placeholder="e.g., +1234567890"
                                onChange={handleChange}
                            />
                        </Form.Group>

                        <div className="mt-3"></div>
                        {!isSubmitted ? (
                            <Button
                                variant="primary"
                                type="submit"
                                className="w-100 transition-button"
                            >
                                {isUpdate ? "Update" : "Create"}
                            </Button>
                        ) : (
                            <Button
                                variant="success"
                                disabled
                                className="w-100 transition-button"
                            >
                                <i className="bi bi-check-lg"></i> Success
                            </Button>
                        )}

                        <div className="mb-3"></div>
                    </Form>
                </Row>
            </Modal.Body>
        </Modal>
    );
};

export default StudentFormModal;
