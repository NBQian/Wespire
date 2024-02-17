import React, { useState, useEffect } from "react";
import { Modal, Row, Form, Button } from "react-bootstrap";
import { addStudent, updateStudent } from "../services/StudentService";

const StudentFormModal = (props) => {
    const { isUpdate, student, setUpdated, onHide, ...modalProps } = props;
    const [isSubmitted, setIsSubmitted] = useState(false);
    useEffect(() => {
        if (!props.show) {
            setIsSubmitted(false);
        }
    }, [props.show]);

    const handleSubmit = (e) => {
        e.preventDefault();
        const formTarget = e.target;

        const action = isUpdate
            ? updateStudent(student.studentId, formTarget)
            : addStudent(formTarget);

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
                <Modal.Title id="contained-modal-title-vcenter">
                    {isUpdate
                        ? "Update Student Information"
                        : "Add Student Information"}
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
                            />
                        </Form.Group>
                        <Form.Group controlId="RegistrationNo">
                            <Form.Label>Registration No.</Form.Label>
                            <Form.Control
                                type="text"
                                name="RegistrationNo"
                                required
                                placeholder=""
                                defaultValue={
                                    isUpdate ? student.RegistrationNo : ""
                                }
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
                            />
                        </Form.Group>
                        <Form.Group controlId="Course">
                            <Form.Label>Course</Form.Label>
                            <Form.Control
                                type="text"
                                name="Course"
                                required
                                placeholder=""
                                defaultValue={isUpdate ? student.Course : ""}
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
