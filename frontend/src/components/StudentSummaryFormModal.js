import React, { useState, useEffect } from "react";
import { Modal, Button, Form, Spinner } from "react-bootstrap";
import { useSelector } from "react-redux";
import {
    addProduct,
    updateProduct,
    getProductsByUniqueCode,
    deleteProduct,
} from "../services/ProductServices";
import {
    addFuturePlan,
    updateFuturePlan,
    getFuturePlansByUniqueCode,
} from "../services/FuturePlanServices";
import {
    addStudentSummary,
    getStudentSummaryById,
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
    Date: null,
    Type: "",
    BasicSum: "",
    TotalDeathCoverage: "",
    TotalPermanentDisability: "",
    EarlyCriticalIllness: "",
    CriticalIllness: "",
    Accidental: "",
    OtherBenefitsRemarks: "",
    Mode: "",
    SinglePaymentAmount: "",
    YearlyPaymentAmount: "",
    PaymentEndDate: null,
    MaturityPremiumEndDate: "",
    CurrentValue: "",
    TotalPremiumsPaid: "",
    PremiumPayoutMode: "",
    PremiumPayoutYear: "",
    PremiumPayoutEndYear: "",
    PremiumPayoutAmount: "",
};

const productFieldLimits = {
    ProductName: 100,
    ProductNumber: 100,
    Company: 100,
    Type: 100,
    Mode: 100,
    SinglePaymentAmount: 10,
    YearlyPaymentAmount: 10,
    MaturityPremiumEndDate: 100,
    BasicSum: 10,
    TotalDeathCoverage: 10,
    TotalPermanentDisability: 10,
    EarlyCriticalIllness: 10,
    Accidental: 10,
    Yearly: 10,
    CurrentValue: 10,
    TotalPremiumsPaid: 11,
    PremiumPayoutAmount: 11,
};

const emptyFuturePlanTemplate = {
    Type: "",
    CurrentSumAssured: "",
    RecommendedSumAssured: "",
    Remarks: "",
};

const futurePlanTypes = [
    "Death",
    "Total Permanent Disability",
    "Critical Illness",
    "Accidental Death & Disablement",
    "Monthly Disability",
];

const singleModes = ["CPF-OA (Single)", "SRS (Single)", "Cash (Single)"];
const yearlyModes = ["Cash (Yearly)", "Cash (Monthly)", "CPF-MA (Yearly)"];
const modeOptions = ["", ...singleModes, ...yearlyModes];
const typeOptions = ["", "Whole Life", "Endowment", "Term", "Inv. Linked"];

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
    const [products, setProducts] = useState([{ ...emptyProductTemplate }]);
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
            }, 500);

            return () => clearInterval(intervalId);
        }
    }, [stage]);

    useEffect(() => {
        if (modalProps.show) {
            const savedAgentData = localStorage.getItem("agentData");
            if (savedAgentData) {
                setAgent([JSON.parse(savedAgentData)]);
            } else if (summary && summary.id) {
                const fetchCurrAgentInfo = async () => {
                    const fetchedSummary = await getStudentSummaryById(
                        summary.id
                    );
                };
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
                setProducts([{ ...emptyProductTemplate }]);
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
        return /^-?\d*(\.\d+)?$/.test(value);
    };

    const isDateValid = (dateString) => {
        // Check if date matches "YYYY-MM-DD" format
        if (dateString === null) {
            return true;
        }
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
        const productDecimalFields = [
            "BasicSum",
            "TotalDeathCoverage",
            "TotalPermanentDisability",
            "EarlyCriticalIllness",
            "CriticalIllness",
            "Accidental",
            "SinglePaymentAmount",
            "YearlyPaymentAmount",
            "CurrentValue",
            "TotalPremiumsPaid",
            "PremiumPayoutAmount",
        ];

        const excludedFields = [
            "Company",
            "Type",
            "ProductNumber",
            "ProductName",
            "Date",
            "OtherBenefitsRemarks",
            "PremiumPayoutMode",
            "PremiumPayoutYear",
            "PremiumPayoutEndYear",
            "PremiumPayoutAmount",
            "PaymentEndDate",
            "MaturityPremiumEndDate",
            ...productDecimalFields,
        ];

        const cover = agent[0];

        for (const key in cover) {
            if (cover[key].trim() === "") {
                return `Please fill out the ${key} field.`;
            }
        }

        for (let i = 0; i < products.length; i++) {
            const product = products[i];
            for (const key of Object.keys(product)) {
                if (!excludedFields.includes(key) && !product[key]) {
                    return `Product ${i + 1}: ${key
                        .replace(/([A-Z])/g, " $1")
                        .replace(/^./, (str) =>
                            str.toUpperCase()
                        )} is required.`;
                }

                if (productDecimalFields.includes(key) && product[key] === "") {
                    product[key] = "0";
                } else if (
                    productDecimalFields.includes(key) &&
                    !isDecimalValid(product[key].toString())
                ) {
                    const msg = `Product ${i + 1}: ${key
                        .replace(/([A-Z])/g, " $1")
                        .replace(/^./, (str) =>
                            str.toUpperCase()
                        )} must be a valid decimal number.`;

                    return msg;
                }
            }
            if (
                (product["Date"] === null || product["Date"] === "") &&
                i == 0
            ) {
                return `Product ${
                    i + 1
                }: Date must be in the format YYYY-MM-DD.`;
            } else if (product["Date"] === "" || product["Date"] === null) {
                product["Date"] = products[i - 1]["Date"];
            }

            if (product["PaymentEndDate"] === "") {
                product["PaymentEndDate"] = null;
            }

            if (
                (product["Mode"].includes("Yearly") ||
                    product["Mode"].includes("Monthly")) &&
                product["PaymentEndDate"] === null
            ) {
                return `Product ${
                    i + 1
                }: Payment End Date must be in the format YYYY-MM-DD.`;
            }

            if (!isDateValid(product["Date"])) {
                return `Product ${
                    i + 1
                }: Date must be in the format YYYY-MM-DD.`;
            }
            if (!isDateValid(product["PaymentEndDate"])) {
                return `Product ${
                    i + 1
                }: Payment End Date must be in the format YYYY-MM-DD.`;
            }
            if (!isDateValid(product["Date"])) {
                return `Product ${
                    i + 1
                }: Premium Payout End Year must be in the format YYYY-MM-DD.`;
            }
        }

        // Validate Future Plan Fields
        const futurePlanDecimalFields = [
            "CurrentSumAssured",
            "RecommendedSumAssured",
        ];

        for (let i = 0; i < futurePlans.length; i++) {
            futurePlanDecimalFields.forEach((field) => {
                if (futurePlans[i][field] === "") {
                    futurePlans[i][field] = "0";
                }
            });

            if (
                !isDecimalValid(
                    futurePlans[i]["CurrentSumAssured"].toString()
                ) ||
                !isDecimalValid(
                    futurePlans[i]["RecommendedSumAssured"].toString()
                )
            ) {
                return `Overall Summary: ${futurePlans[i].Type} - Both Current Sum Assured and Recommended Sum Assured must be valid decimal numbers.`;
            }

            if (
                parseFloat(futurePlans[i]["CurrentSumAssured"]) >
                parseFloat(futurePlans[i]["RecommendedSumAssured"])
            ) {
                return `Overall Summary: ${futurePlans[i].Type} - Current Sum Assured must be less than or equal to Recommended Sum Assured.`;
            }
        }

        // If all fields are validated
        return "";
    };

    const handleAgentChange = (event) => {
        const newagent = [...agent];
        newagent[0][event.target.name] = event.target.value;
        setAgent(newagent);
    };

    const handleProductChange = (event) => {
        const { name, value } = event.target;
        const updatedProducts = [...products];

        // If changing PremiumPayoutMode to "Yearly", reset PremiumPayoutYear
        if (name === "PremiumPayoutMode" && value === "NA") {
            updatedProducts[currentPage]["PremiumPayoutYear"] = "";
            updatedProducts[currentPage]["PremiumPayoutEndYear"] = "";
            updatedProducts[currentPage]["PremiumPayoutAmount"] = "";
        }

        if (name === "Mode" && !singleModes.includes(value)) {
            updatedProducts[currentPage]["SinglePaymentAmount"] = "";
        }

        if (name === "Mode" && !yearlyModes.includes(value)) {
            updatedProducts[currentPage]["YearlyPaymentAmount"] = "";
        }

        // Update the changed field with the new value
        updatedProducts[currentPage][name] = value;

        // Apply the updates to the state
        setProducts(updatedProducts);
    };

    const handleFuturePlanChange = (event) => {
        const updatedPlans = [...futurePlans];
        updatedPlans[currentPage][event.target.name] = event.target.value;
        setFuturePlans(updatedPlans);
    };

    const addNewProduct = () => {
        const validationMessage = validateFields();
        if (validationMessage !== "") {
            alert(validationMessage);
            return;
        }
        setProducts([...products, { ...emptyProductTemplate }]);
        setCurrentPage(products.length);
    };

    const goToPreviousItem = () => {
        const validationMessage = validateFields();
        if (validationMessage !== "") {
            alert(validationMessage);
            return;
        }
        setCurrentPage(currentPage - 1);
    };

    const goToNextItem = () => {
        const validationMessage = validateFields();
        if (validationMessage !== "") {
            alert(validationMessage);
            return;
        }
        setCurrentPage(currentPage + 1);
    };

    const removeCurrentProduct = () => {
        const product = products[currentPage];
        if (product.id) {
            deleteProduct(product.id);
        }
        const updatedProducts = products.filter(
            (_, index) => index !== currentPage
        );
        setProducts(updatedProducts);
        setCurrentPage(Math.max(currentPage - 1, 0));
    };

    const switchToAgent = () => {
        const validationMessage = validateFields();
        if (validationMessage !== "") {
            alert(validationMessage);
            return;
        }
        setStage("agent");
    };

    const switchToFuturePlans = () => {
        const validationMessage = validateFields();
        if (validationMessage !== "") {
            alert(validationMessage);
            return;
        }
        setStage("futurePlans");
        setCurrentPage(0);
    };

    const switchToProducts = () => {
        // const validationMessage = validateFields();
        // if (validationMessage !== "") {
        //     alert(validationMessage);
        //     return;
        // }
        setStage("products");
        setCurrentPage(products.length - 1);
    };

    const submitAll = async (e) => {
        localStorage.setItem("agentData", JSON.stringify(agent[0]));
        e.preventDefault(); // Prevent default form submission

        const validationMessage = validateFields();
        if (validationMessage !== "") {
            alert(validationMessage);
            return;
        }
        setStage("loading");

        try {
            const productPromises = products.map((product) =>
                product.id
                    ? updateProduct(product.id, {
                          ...product,
                          unique_code: code,
                      })
                    : addProduct({ ...product, unique_code: code })
            );
            await Promise.all(productPromises);

            const futurePlanPromises = futurePlans.map((plan) => {
                const shortfall =
                    plan.RecommendedSumAssured - plan.CurrentSumAssured;
                const planData = {
                    ...plan,
                    unique_code: code,
                    Shortfall: shortfall,
                };

                return plan.id
                    ? updateFuturePlan(plan.id, planData)
                    : addFuturePlan(planData);
            });
            await Promise.all(futurePlanPromises);

            if (isUpdate && summary.id) {
                await updateStudentSummary(summary.id, {
                    ...agent[0],
                    student: summary.student.studentId,
                });
                setUpdated(true);
            } else {
                await addStudentSummary({
                    ...agent[0],
                    unique_code: code,
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
            backdrop={stage === "loading" ? "static" : true}
            keyboard={stage !== "loading"}
        >
            {stage !== "loading" && stage !== "success" ? (
                <Modal.Header closeButton>
                    <Modal.Title
                        id="contained-modal-title-vcenter"
                        className="centered-modal-title"
                    >
                        {stage === "agent" && "Agent Information"}
                        {stage === "products" &&
                            `Product ${currentPage + 1} Details`}
                        {stage === "futurePlans" && (
                            <div>
                                Overall Coverage Summary: <br />
                                {futurePlans[currentPage]["Type"]}
                            </div>
                        )}
                    </Modal.Title>
                </Modal.Header>
            ) : (
                <Modal.Header>
                    <Modal.Title
                        id="contained-modal-title-vcenter"
                        className="centered-modal-title"
                    >
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
                                <Form.Group key={field} className="mb-3">
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
                                    <Form.Group key={field} className="mb-3">
                                        <Form.Label>
                                            Other Benefits / Remarks
                                        </Form.Label>
                                        <Form.Control
                                            as="textarea"
                                            rows={3}
                                            name={field}
                                            value={
                                                products[currentPage][field] ||
                                                ""
                                            }
                                            onChange={handleProductChange}
                                            style={{
                                                resize: "none",
                                            }}
                                        />
                                    </Form.Group>
                                );
                            }
                            // Special handling for the Date field
                            if (field === "Date") {
                                return (
                                    <Form.Group key={field} className="mb-3">
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
                                            showYearDropdown
                                            yearDropdownItemNumber={40}
                                            scrollableYearDropdown
                                        />
                                    </Form.Group>
                                );
                            }

                            if (field === "Type") {
                                return (
                                    <Form.Group key={field} className="mb-3">
                                        <Form.Label>{label}</Form.Label>
                                        <Form.Control
                                            as="select"
                                            name={field}
                                            value={
                                                products[currentPage][field] ||
                                                ""
                                            }
                                            onChange={handleProductChange}
                                        >
                                            {typeOptions.map(
                                                (optionValue, index) => {
                                                    const label =
                                                        optionValue === ""
                                                            ? "Select an option"
                                                            : optionValue;
                                                    return (
                                                        <option
                                                            key={index}
                                                            value={optionValue}
                                                        >
                                                            {label}
                                                        </option>
                                                    );
                                                }
                                            )}
                                        </Form.Control>
                                    </Form.Group>
                                );
                            }

                            if (field === "Mode") {
                                return (
                                    <Form.Group key={field} className="mb-3">
                                        <Form.Label>{label}</Form.Label>
                                        <Form.Control
                                            as="select"
                                            name={field}
                                            value={
                                                products[currentPage][field] ||
                                                ""
                                            }
                                            onChange={handleProductChange}
                                        >
                                            {modeOptions.map(
                                                (optionValue, index) => {
                                                    const label =
                                                        optionValue === ""
                                                            ? "Select an option"
                                                            : optionValue;
                                                    return (
                                                        <option
                                                            key={index}
                                                            value={optionValue}
                                                        >
                                                            {label}
                                                        </option>
                                                    );
                                                }
                                            )}
                                        </Form.Control>
                                    </Form.Group>
                                );
                            }

                            if (field === "SinglePaymentAmount") {
                                const isSinglePaymentEnabled =
                                    singleModes.includes(
                                        products[currentPage]["Mode"]
                                    );
                                return (
                                    <Form.Group
                                        key="SinglePaymentAmount"
                                        className="mb-3"
                                    >
                                        <Form.Label>{label}</Form.Label>
                                        <Form.Control
                                            type="text"
                                            name="SinglePaymentAmount"
                                            value={
                                                products[currentPage][
                                                    "SinglePaymentAmount"
                                                ] || ""
                                            }
                                            onChange={handleProductChange}
                                            disabled={!isSinglePaymentEnabled}
                                            maxLength={
                                                productFieldLimits[field]
                                            }
                                        />
                                    </Form.Group>
                                );
                            }

                            if (field === "YearlyPaymentAmount") {
                                const isYearlyPaymentEnabled =
                                    yearlyModes.includes(
                                        products[currentPage]["Mode"]
                                    );
                                return (
                                    <Form.Group
                                        key="YearlyPaymentAmount"
                                        className="mb-3"
                                    >
                                        <Form.Label>
                                            Monthly / Yearly Payment Amount
                                        </Form.Label>
                                        <Form.Control
                                            type="text"
                                            name="YearlyPaymentAmount"
                                            value={
                                                products[currentPage][field] ||
                                                ""
                                            }
                                            onChange={handleProductChange}
                                            disabled={!isYearlyPaymentEnabled}
                                            maxLength={
                                                productFieldLimits[field]
                                            }
                                        />
                                    </Form.Group>
                                );
                            }

                            if (field === "PaymentEndDate") {
                                const isYearlyPaymentEnabled =
                                    yearlyModes.includes(
                                        products[currentPage]["Mode"]
                                    );
                                return (
                                    isYearlyPaymentEnabled && (
                                        <Form.Group
                                            key={field}
                                            className="mb-3"
                                        >
                                            <Form.Label>{label}</Form.Label>
                                            <ReactDatePicker
                                                selected={
                                                    products[currentPage][field]
                                                        ? new Date(
                                                              products[
                                                                  currentPage
                                                              ][field]
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
                                                showYearDropdown
                                                yearDropdownItemNumber={40}
                                                scrollableYearDropdown
                                            />
                                        </Form.Group>
                                    )
                                );
                            }

                            if (field === "PremiumPayoutMode") {
                                return (
                                    <Form.Group key={field} className="mb-3">
                                        <Form.Label>{label}</Form.Label>
                                        <Form.Control
                                            as="select"
                                            name={field}
                                            value={
                                                products[currentPage][field] ||
                                                "NA"
                                            }
                                            onChange={handleProductChange}
                                        >
                                            <option value="NA">NA</option>
                                            <option value="Yearly">
                                                Yearly
                                            </option>
                                            <option value="Single">
                                                Single
                                            </option>
                                        </Form.Control>
                                    </Form.Group>
                                );
                            }

                            if (field === "PremiumPayoutYear") {
                                const currentYear = new Date().getFullYear();
                                const startYear = currentYear - 50;
                                const endYear = currentYear + 25;

                                const isDisabled =
                                    products[currentPage][
                                        "PremiumPayoutMode"
                                    ] !== "Single" &&
                                    products[currentPage][
                                        "PremiumPayoutMode"
                                    ] !== "Yearly";
                                return (
                                    <Form.Group key={field} className="mb-3">
                                        <Form.Label>
                                            {products[currentPage][
                                                "PremiumPayoutMode"
                                            ] === "Single"
                                                ? "Single Payout Year"
                                                : products[currentPage][
                                                      "PremiumPayoutMode"
                                                  ] === "Yearly"
                                                ? "Payout Starting Year"
                                                : "Payout Year"}
                                        </Form.Label>

                                        <Form.Control
                                            as="select"
                                            name={field}
                                            value={
                                                products[currentPage][field] ||
                                                ""
                                            }
                                            onChange={handleProductChange}
                                            disabled={isDisabled}
                                        >
                                            <option value="">
                                                Select a year
                                            </option>
                                            {[
                                                ...Array(
                                                    endYear - startYear + 1
                                                ).keys(),
                                            ].map((i) => (
                                                <option
                                                    key={i}
                                                    value={startYear + i}
                                                >
                                                    {startYear + i}
                                                </option>
                                            ))}
                                        </Form.Control>
                                    </Form.Group>
                                );
                            }

                            if (field === "PremiumPayoutEndYear") {
                                const currentYear = new Date().getFullYear();
                                const startYear = currentYear - 5;
                                const endYear = currentYear + 100;

                                const isDisabled =
                                    products[currentPage][
                                        "PremiumPayoutMode"
                                    ] !== "Yearly";
                                return (
                                    <Form.Group key={field} className="mb-3">
                                        <Form.Label>{label}</Form.Label>

                                        <Form.Control
                                            as="select"
                                            name={field}
                                            value={
                                                products[currentPage][field] ||
                                                ""
                                            }
                                            onChange={handleProductChange}
                                            disabled={isDisabled}
                                        >
                                            <option value="">
                                                Select a year
                                            </option>
                                            {[
                                                ...Array(
                                                    endYear - startYear + 1
                                                ).keys(),
                                            ].map((i) => (
                                                <option
                                                    key={i}
                                                    value={startYear + i}
                                                >
                                                    {startYear + i}
                                                </option>
                                            ))}
                                        </Form.Control>
                                    </Form.Group>
                                );
                            }
                            if (field === "PremiumPayoutAmount") {
                                const isDisabled =
                                    products[currentPage][
                                        "PremiumPayoutMode"
                                    ] === null ||
                                    products[currentPage][
                                        "PremiumPayoutMode"
                                    ] === "NA";

                                return (
                                    <Form.Group key={field} className="mb-3">
                                        <Form.Label>{label}</Form.Label>
                                        <Form.Control
                                            type="text"
                                            name={field}
                                            value={
                                                products[currentPage][field] ||
                                                ""
                                            }
                                            onChange={handleProductChange}
                                            disabled={isDisabled}
                                        />
                                    </Form.Group>
                                );
                            }

                            return (
                                <Form.Group key={field} className="mb-3">
                                    <Form.Label>{label}</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name={field}
                                        value={
                                            products[currentPage][field] || ""
                                        }
                                        maxLength={productFieldLimits[field]}
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
                            if (field === "Type") return null;

                            const label = field
                                .replace(/([A-Z])/g, " $1")
                                .replace(/^./, (str) => str.toUpperCase());

                            if (field === "Remarks") {
                                return (
                                    <Form.Group key={field} className="mb-3">
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
                                <Form.Group key={field} className="mb-3">
                                    <Form.Label>{label}</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name={field}
                                        value={
                                            futurePlans[currentPage][field] ||
                                            ""
                                        }
                                        onChange={handleFuturePlanChange}
                                        maxLength={13}
                                    />
                                </Form.Group>
                            );
                        })}
                        <div className="d-flex justify-content-between mt-3">
                            {currentPage === 0 ? (
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
