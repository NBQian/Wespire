import React, { useState, useEffect } from "react";
import { Modal, Row, Form, Button } from "react-bootstrap";
import {
    addStudentSummary,
    updateStudentSummary,
} from "../services/StudentSummaryService";
import { useSelector } from "react-redux";

const StudentSummaryFormModal = (props) => {
    const { summary, isUpdate, setUpdated, student, onHide, ...modalProps } =
        props;
    const [isSubmitted, setIsSubmitted] = useState(false);

    const userId = useSelector((state) => state.auth.user.id);
    const code = `${userId}-${Date.now()}`;
    console.log(code);

    function calculatePercentage(coursesPassed, coursesFailed) {
        const totalCourses =
            parseInt(coursesPassed, 10) + parseInt(coursesFailed, 10);
        return totalCourses > 0
            ? (parseInt(coursesPassed, 10) / totalCourses) * 100
            : 0;
    }

    useEffect(() => {
        if (!props.show) {
            setIsSubmitted(false);
        }
    }, [props.show]);

    const handleSubmit = (e) => {
        console.log(code);
        e.preventDefault();
        const formTarget = e.target;
        const summaryData = {
            student:
                summary && summary.student
                    ? summary.student.studentId
                    : student.studentId,
            percentage_courses_passed: calculatePercentage(
                formTarget.coursesPassed.value,
                formTarget.coursesFailed.value
            ),
        };

        const action = isUpdate
            ? updateStudentSummary(summary.id, summaryData)
            : addStudentSummary(summaryData);

        action.then(
            (result) => {
                setIsSubmitted(true);
                setTimeout(() => {
                    props.setUpdated(true);
                    props.onHide();
                }, 500);
            },
            (error) => {
                alert(
                    isUpdate
                        ? "Failed to Update Summary"
                        : "Failed to Add Summary"
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
            <Modal.Header>
                <Modal.Title id="contained-modal-title-vcenter">
                    Add Student Summary
                </Modal.Title>
                <Button variant="danger" onClick={onHide} className="ms-auto">
                    Cancel
                </Button>
            </Modal.Header>

            <Modal.Body>
                <Row>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group controlId="coursesPassed">
                            <Form.Label>Courses Passed</Form.Label>
                            <Form.Control
                                type="number"
                                name="coursesPassed"
                                required
                                placeholder="Number of courses passed"
                            />
                        </Form.Group>
                        <Form.Group controlId="coursesFailed">
                            <Form.Label>Courses Failed</Form.Label>
                            <Form.Control
                                type="number"
                                name="coursesFailed"
                                required
                                placeholder="Number of courses failed"
                            />
                        </Form.Group>

                        <div className="mt-3"></div>
                        {!isSubmitted ? (
                            <Button
                                variant="primary"
                                type="submit"
                                className="w-100 transition-button"
                            >
                                Submit
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

export default StudentSummaryFormModal;
