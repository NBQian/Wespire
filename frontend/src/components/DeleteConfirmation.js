import React, { useState } from "react";
import { Modal, Button } from "react-bootstrap";

const DeleteConfirmation = ({ show, onConfirm, onCancel }) => {
    const [isDeleted, setIsDeleted] = useState(false);

    const handleConfirm = () => {
        onConfirm();
        setIsDeleted(true); // Set deletion status to true upon confirmation
    };

    return (
        <Modal
            show={show}
            onHide={onCancel}
            onExited={() => setIsDeleted(false)}
        >
            <Modal.Header>
                <Modal.Title>Confirm Deletion</Modal.Title>
                <Button variant="secondary" onClick={onCancel}>
                    Cancel
                </Button>
            </Modal.Header>
            <Modal.Body>
                Are you sure you want to delete this Client?
            </Modal.Body>
            <Modal.Footer>
                {!isDeleted ? (
                    <Button
                        variant="danger"
                        onClick={handleConfirm}
                        className="w-100"
                    >
                        Delete
                    </Button>
                ) : (
                    <Button
                        variant="success"
                        disabled
                        className="w-100 transition-button"
                    >
                        Deleted Successfully
                    </Button>
                )}
            </Modal.Footer>
        </Modal>
    );
};

export default DeleteConfirmation;
