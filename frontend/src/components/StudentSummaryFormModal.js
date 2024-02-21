import React, { useState, useEffect, useRef } from "react";
import { Modal, Button, Form, Spinner } from "react-bootstrap";
import { useSelector } from "react-redux";
import {
    addProduct,
    updateProduct,
    getProductsByUniqueCode,
} from "../services/ProductServices";
import {
    addFuturePlan,
    updateFuturePlan,
    getFuturePlansByUniqueCode,
} from "../services/FuturePlanServices";
import {
    addStudentSummary,
    updateStudentSummary,
} from "../services/StudentSummaryService";
import ReactDatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import GreenTick from "../static/check.png";

const emptySummaryTemplate = {
    DisplayedName: "",
    DisplayedPhoneNumber: "",
    DisplayedEmail: "",
    DisplayedTitle: "",
    MAS: "",
};
const emptyProductTemplate = {
    Company: "",
    ProductNumber: "",
    ProductName: "",
    Date: "",
    Type: "",
    WholeLife: "",
    Endowment: "",
    Term: "",
    InvLinked: "",
    TotalDeathCoverage: "",
    TotalPermanentDisability: "",
    EarlyCriticalIllness: "",
    Accidental: "",
    OtherBenefitsRemarks: "",
    Mode: "",
    Monthly: "",
    Quarterly: "",
    SemiAnnual: "",
    Yearly: "",
    MaturityPremiumEndDate: "",
    CurrentValue: "",
    TotalPremiumsPaid: "",
};

const emptyFuturePlanTemplate = {
    Type: "",
    CurrentSumAssured: "",
    RecommendedSumAssured: "",
    Shortfall: "",
    Remarks: "",
};

const futurePlanTypes = [
    "Death",
    "Total Permanent Disability",
    "Critical Illness",
    "Accidental Death & Disablement",
    "Monthly Disability",
];

const StudentSummaryFormModal = ({
    student,
    onHide,
    isUpdate,
    setUpdated,
    summary,
    ...modalProps
}) => {
    const userId = useSelector((state) => state.auth.user.id);
    const [code, setCode] = useState("");
    const [agent, setAgent] = useState([emptySummaryTemplate]);
    const [products, setProducts] = useState([emptyProductTemplate]);
    const [futurePlans, setFuturePlans] = useState([emptyFuturePlanTemplate]);
    const [currentPage, setCurrentPage] = useState(0);
    const [stage, setStage] = useState("agent");

    const [ellipsis, setEllipsis] = useState("");

    useEffect(() => {
        if (stage === "loading") {
            const intervalId = setInterval(() => {
                setEllipsis((prevEllipsis) =>
                    prevEllipsis.length < 16 ? prevEllipsis + ". " : "  "
                );
            }, 500); // Adjust timing as needed

            return () => clearInterval(intervalId);
        }
    }, [stage]);

    useEffect(() => {
        if (modalProps.show) {
            const savedAgentData = localStorage.getItem("agentData");
            if (savedAgentData) {
                setAgent([JSON.parse(savedAgentData)]);
            } else {
                setAgent([emptySummaryTemplate]); // Reset to empty template if no saved data
            }
            if (isUpdate && summary) {
                setCode(summary.unique_code); // Use existing unique_code for editing
                // Fetch data for editing
                const fetchEditData = async () => {
                    const fetchedProducts = await getProductsByUniqueCode(
                        summary.unique_code
                    );
                    const fetchedFuturePlans = await getFuturePlansByUniqueCode(
                        summary.unique_code
                    );
                    setProducts(
                        fetchedProducts.length
                            ? fetchedProducts
                            : [emptyProductTemplate]
                    );
                    setFuturePlans(
                        fetchedFuturePlans.length
                            ? fetchedFuturePlans
                            : futurePlanTypes.map((type) => ({
                                  ...emptyFuturePlanTemplate,
                                  Type: type,
                              }))
                    );
                    setCurrentPage(0);
                };
                fetchEditData();
            } else {
                // Setup for adding new entry
                const newCode = `${userId}-${Date.now()}`;
                setCode(newCode);
                setProducts([emptyProductTemplate]);
                setFuturePlans(
                    futurePlanTypes.map((type) => ({
                        ...emptyFuturePlanTemplate,
                        Type: type,
                    }))
                );
                setCurrentPage(0);
            }
        } else {
            // Reset to initial state when modal is hidden
            setProducts([emptyProductTemplate]);
            setFuturePlans(
                futurePlanTypes.map((type) => ({
                    ...emptyFuturePlanTemplate,
                    Type: type,
                }))
            );
            setCurrentPage(0);
            setStage("agent");
        }
    }, [modalProps.show]);

    const isDecimalValid = (value) => {
        return /^-?\d*(\.\d+)?$/.test(value); // Matches decimal numbers, including negative and positive
    };

    const isDateValid = (dateString) => {
        // Check if date matches "YYYY-MM-DD" format
        if (!/^\d{4}-\d{2}-\d{2}$/.test(dateString)) {
            return false;
        }

        // Try parsing the date to ensure it's a valid date
        const date = new Date(dateString);
        const timestamp = date.getTime();

        // Check if the date is not NaN and the dateString is not converting some invalid date to a valid one
        if (!isNaN(timestamp) && date.toISOString().startsWith(dateString)) {
            return true;
        }
        return false;
    };

    const validateFields = () => {
        // Validate Product Fields
        const decimalFields1 = [
            "WholeLife",
            "Endowment",
            "Term",
            "InvLinked",
            "TotalDeathCoverage",
            "TotalPermanentDisability",
            "EarlyCriticalIllness",
            "Accidental",
            "Monthly",
            "Quarterly",
            "SemiAnnual",
            "Yearly",
            "CurrentValue",
            "TotalPremiumsPaid",
        ];

        for (let i = 0; i < products.length; i++) {
            for (let key in products[i]) {
                if (products[i][key] === "") {
                    return `Product ${i + 1}: ${key
                        .replace(/([A-Z])/g, " $1")
                        .replace(/^./, (str) =>
                            str.toUpperCase()
                        )} is missing.`;
                } else if (decimalFields1.includes(key)) {
                    if (!isDecimalValid(products[i][key].toString())) {
                        return `Product ${i + 1}: ${key
                            .replace(/([A-Z])/g, " $1")
                            .replace(/^./, (str) =>
                                str.toUpperCase()
                            )} must be a valid decimal number.`;
                    }
                }
            }
            if (!isDateValid(products[i]["Date"])) {
                return `Product ${
                    i + 1
                }: Date must be in the format YYYY-MM-DD.`;
            }
        }

        // Validate Future Plan Fields
        const decimalFields2 = [
            "CurrentSumAssured",
            "RecommendedSumAssured",
            "Shortfall",
        ];

        for (let i = 0; i < futurePlans.length; i++) {
            for (let key in futurePlans[i]) {
                if (futurePlans[i][key] === "") {
                    // Assuming the Type field is always filled for future plans. Adjust if necessary.
                    return `Overall Summary: ${futurePlans[i].Type} - ${key
                        .replace(/([A-Z])/g, " $1")
                        .replace(/^./, (str) =>
                            str.toUpperCase()
                        )} is missing.`;
                } else if (decimalFields2.includes(key)) {
                    if (!isDecimalValid(futurePlans[i][key].toString())) {
                        return `Overall Summary: ${futurePlans[i].Type} - ${key
                            .replace(/([A-Z])/g, " $1")
                            .replace(/^./, (str) =>
                                str.toUpperCase()
                            )} must be a valid decimal number.`;
                    }
                }
            }
        }

        // If all fields are filled
        return "";
    };

    const handleAgentChange = (event) => {
        const newagent = [...agent];
        newagent[0][event.target.name] = event.target.value;
        setAgent(newagent);
    };

    const handleProductChange = (event) => {
        const updatedProducts = [...products];
        updatedProducts[currentPage][event.target.name] = event.target.value;
        setProducts(updatedProducts);
    };

    const handleFuturePlanChange = (event) => {
        const updatedPlans = [...futurePlans];
        updatedPlans[currentPage][event.target.name] = event.target.value;
        setFuturePlans(updatedPlans);
    };

    const addNewProduct = () => {
        setProducts([...products, { ...emptyProductTemplate }]);
        setCurrentPage(products.length);
    };

    const goToPreviousItem = () => {
        setCurrentPage(currentPage - 1);
    };

    const goToNextItem = () => {
        setCurrentPage(currentPage + 1);
    };

    const removeCurrentProduct = () => {
        const updatedProducts = products.filter(
            (_, index) => index !== currentPage
        );
        setProducts(updatedProducts);
        setCurrentPage(Math.max(currentPage - 1, 0));
    };

    const switchToAgent = () => {
        setStage("agent");
    };

    const switchToFuturePlans = () => {
        setStage("futurePlans");
        setCurrentPage(0);
    };

    const switchToProducts = () => {
        setStage("products");
        setCurrentPage(products.length - 1);
    };

    const submitAll = async (e) => {
        localStorage.setItem("agentData", JSON.stringify(agent[0]));
        e.preventDefault(); // Prevent default form submission

        const validationMessage = validateFields();
        if (validationMessage !== "") {
            alert(validationMessage); // Alert the user to fill in the missing fields
            return; // Prevent form submission
        }
        setStage("loading");
        try {
            // Handle products: update existing or add new ones
            const productPromises = products.map((product) =>
                product.id
                    ? updateProduct(product.id, {
                          ...product,
                          unique_code: code,
                      }) // Assumes product.id is available for existing products
                    : addProduct({ ...product, unique_code: code })
            );
            await Promise.all(productPromises);

            // Handle future plans: update existing or add new ones
            const futurePlanPromises = futurePlans.map((plan) =>
                plan.id
                    ? updateFuturePlan(plan.id, { ...plan, unique_code: code }) // Assumes plan.id is available for existing future plans
                    : addFuturePlan({ ...plan, unique_code: code })
            );
            await Promise.all(futurePlanPromises);

            // Update the student summary if editing
            if (isUpdate && summary.id) {
                const readyAgent = agent[0];
                await updateStudentSummary(summary.id, {
                    ...agent[0],
                    student: summary.student.studentId,
                });
                setUpdated(true);
            } else {
                // Create the student summary if adding new

                await addStudentSummary({
                    ...agent[0],
                    // Assuming addStudentSummary doesn't need an id and creates a new entry.
                    unique_code: code,
                    // Include other necessary fields for creating a student summary.
                    student: student.studentId,
                });
            }
            setStage("success");
            setTimeout(() => {
                onHide();
                setStage("agent");
            }, 1000);
        } catch (error) {
            console.error("Error submitting data: ", error);
        }
    };

    return (
        <Modal
            {...modalProps}
            aria-labelledby="contained-modal-title-vcenter"
            centered
            onHide={onHide}
            backdrop={stage === "loading" ? "static" : true} // Prevent closing by clicking outside when loading
            keyboard={stage !== "loading"}
        >
            {stage !== "loading" && stage !== "success" ? (
                // Render Modal.Header with closeButton when stage is not "loading" or "success"
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        {/* Title based on stage */}
                    </Modal.Title>
                </Modal.Header>
            ) : (
                // Render Modal.Header without closeButton when stage is "loading" or "success"
                <Modal.Header>
                    <Modal.Title
                        id="contained-modal-title-vcenter"
                        className="centered-modal-title"
                    >
                        {stage === "agent" && "Agent Information"}
                        {stage === "products" &&
                            `Product Details - ${currentPage + 1}`}
                        {stage === "futurePlans" && "Overall Coverage Summary"}
                        {stage === "loading" && (
                            <div>Generating Report{ellipsis}</div>
                        )}
                        {stage === "success" && "Success !"}
                    </Modal.Title>
                </Modal.Header>
            )}
            <Modal.Body>
                {stage === "loading" && (
                    <div className="text-center">
                        <Spinner animation="border" role="status">
                            <span className="visually-hidden">Loading...</span>
                        </Spinner>
                    </div>
                )}

                {stage === "success" && (
                    <div className="text-center">
                        <img
                            src={GreenTick}
                            alt="Success"
                            style={{ width: "100px", height: "100px" }}
                        />
                    </div>
                )}

                {stage === "agent" && (
                    <Form onSubmit={submitAll}>
                        {Object.keys(emptySummaryTemplate).map((field) => {
                            const label = field
                                .replace(/([A-Z])/g, " $1")
                                .replace(/^./, (str) => str.toUpperCase());
                            return (
                                <Form.Group key={field}>
                                    <Form.Label>{label}</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name={field}
                                        value={agent[0][field] || ""}
                                        onChange={handleAgentChange}
                                    />
                                </Form.Group>
                            );
                        })}
                        <div className="d-flex justify-content-between mt-3">
                            <Button
                                variant="secondary"
                                onClick={switchToProducts}
                            >
                                Edit Products
                            </Button>
                        </div>
                        {isUpdate && (
                            <Button
                                variant="success"
                                type="submit"
                                className="w-100 mt-3"
                            >
                                Submit All
                            </Button>
                        )}
                    </Form>
                )}
                {stage === "products" && (
                    <Form onSubmit={submitAll}>
                        {Object.keys(emptyProductTemplate).map((field) => {
                            const label = field
                                .replace(/([A-Z])/g, " $1")
                                .replace(/^./, (str) => str.toUpperCase());
                            if (field === "OtherBenefitsRemarks") {
                                return (
                                    <Form.Group key={field}>
                                        <Form.Label>{label}</Form.Label>
                                        <Form.Control
                                            as="textarea"
                                            rows={3} // Starting rows
                                            name={field}
                                            value={
                                                products[currentPage][field] ||
                                                ""
                                            }
                                            onChange={handleProductChange}
                                            style={{
                                                resize: "none",
                                            }} // Optional: Prevent manual resizing
                                        />
                                    </Form.Group>
                                );
                            }
                            // Special handling for the Date field
                            if (field === "Date") {
                                return (
                                    <Form.Group key={field}>
                                        <Form.Label>{label}</Form.Label>
                                        <ReactDatePicker
                                            selected={
                                                products[currentPage][field]
                                                    ? new Date(
                                                          products[currentPage][
                                                              field
                                                          ]
                                                      )
                                                    : null
                                            }
                                            onChange={(date) => {
                                                const newProducts = [
                                                    ...products,
                                                ];
                                                newProducts[currentPage][
                                                    field
                                                ] = date
                                                    ? date
                                                          .toISOString()
                                                          .split("T")[0]
                                                    : "";
                                                setProducts(newProducts);
                                            }}
                                            dateFormat="yyyy-MM-dd"
                                            className="form-control custom-datepicker"
                                            placeholderText="Select date"
                                        />
                                    </Form.Group>
                                );
                            }

                            // Default handling for other fields
                            return (
                                <Form.Group key={field}>
                                    <Form.Label>{label}</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name={field}
                                        value={
                                            products[currentPage][field] || ""
                                        }
                                        onChange={handleProductChange}
                                    />
                                </Form.Group>
                            );
                        })}

                        <div className="d-flex justify-content-between mt-3">
                            {currentPage === 0 ? (
                                <Button
                                    variant="secondary"
                                    onClick={switchToAgent}
                                >
                                    Edit Agent Info
                                </Button>
                            ) : (
                                <Button
                                    variant="secondary"
                                    onClick={goToPreviousItem}
                                >
                                    Previous
                                </Button>
                            )}

                            <Button
                                variant="danger"
                                onClick={removeCurrentProduct}
                                disabled={products.length === 1}
                            >
                                Remove Current Product
                            </Button>
                            {currentPage === products.length - 1 ? (
                                <Button
                                    variant="primary"
                                    onClick={addNewProduct}
                                >
                                    Add Another Product
                                </Button>
                            ) : (
                                <Button
                                    variant="secondary"
                                    onClick={goToNextItem}
                                >
                                    Next
                                </Button>
                            )}
                        </div>
                        {currentPage === products.length - 1 && (
                            <Button onClick={switchToFuturePlans}>
                                Edit Overall Summary
                            </Button>
                        )}
                        {isUpdate && (
                            <Button
                                variant="success"
                                type="submit"
                                className="w-100 mt-3"
                            >
                                Submit All
                            </Button>
                        )}
                    </Form>
                )}
                {stage === "futurePlans" && (
                    <Form onSubmit={submitAll}>
                        {Object.keys(emptyFuturePlanTemplate).map((field) => {
                            if (field === "Type") return null; // Skip rendering the "Type" field

                            const label = field
                                .replace(/([A-Z])/g, " $1")
                                .replace(/^./, (str) => str.toUpperCase());

                            if (field === "Remarks") {
                                return (
                                    <Form.Group key={field}>
                                        <Form.Label>{label}</Form.Label>
                                        <Form.Control
                                            as="textarea"
                                            rows={3} // Starting rows
                                            name={field}
                                            value={
                                                futurePlans[currentPage][
                                                    field
                                                ] || ""
                                            }
                                            onChange={handleFuturePlanChange}
                                            style={{
                                                resize: "none",
                                            }} // Optional: Prevent manual resizing
                                        />
                                    </Form.Group>
                                );
                            }
                            return (
                                <Form.Group key={field}>
                                    <Form.Label>{label}</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name={field}
                                        value={
                                            futurePlans[currentPage][field] ||
                                            ""
                                        }
                                        onChange={handleFuturePlanChange}
                                    />
                                </Form.Group>
                            );
                        })}
                        <div className="d-flex justify-content-between mt-3">
                            {currentPage == 0 ? (
                                <Button
                                    variant="secondary"
                                    onClick={switchToProducts}
                                >
                                    Edit Products
                                </Button>
                            ) : (
                                <Button
                                    variant="secondary"
                                    onClick={goToPreviousItem}
                                >
                                    Previous
                                </Button>
                            )}
                            {currentPage < futurePlans.length - 1 && (
                                <Button
                                    variant="secondary"
                                    onClick={goToNextItem}
                                >
                                    Next
                                </Button>
                            )}
                        </div>
                        {(currentPage === futurePlans.length - 1 ||
                            isUpdate) && (
                            <Button
                                variant="success"
                                type="submit"
                                className="w-100 mt-3"
                            >
                                Submit All
                            </Button>
                        )}
                    </Form>
                )}
            </Modal.Body>
        </Modal>
    );
};

export default StudentSummaryFormModal;
