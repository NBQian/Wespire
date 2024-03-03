import React, { useMemo, useState, useEffect } from "react";
import {
    MaterialReactTable,
    useMaterialReactTable,
    MRT_ToggleFiltersButton,
} from "material-react-table";
import {
    Box,
    Typography,
    Button,
    MenuItem,
    ListItemIcon,
    lighten,
} from "@mui/material";
import StudentFormModal from "./StudentFormModal";
import DeleteConfirmation from "./DeleteConfirmation";
import { getStudents, deleteStudent } from "../services/StudentService";
import StudentSummaryFormModal from "./StudentSummaryFormModal";
import { Edit, Delete, NoteAdd } from "@mui/icons-material";

const StudentList = () => {
    const [students, setStudents] = useState([]);
    const [modalShow, setModalShow] = useState(false);
    const [currentStudent, setCurrentStudent] = useState(null);
    const [isUpdated, setIsUpdated] = useState(false);
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
    const [studentToDelete, setStudentToDelete] = useState(null);
    const [showSummaryModal, setShowSummaryModal] = useState(false);
    const [currentStudentForSummary, setCurrentStudentForSummary] =
        useState(null);
    useEffect(() => {
        getStudents().then((data) => {
            setStudents(data);
            setIsUpdated(false);
        });
    }, [isUpdated]);

    const columns = useMemo(
        () => [
            {
                accessorKey: "FirstName",
                header: "First Name",
                size: 100,
                flex: 1,
            },
            {
                accessorKey: "LastName",
                header: "Last Name",
                size: 100,
                flex: 1,
            },
            {
                accessorKey: "Email",
                header: "Email",
                enableClickToCopy: true,
                size: 250,
                flex: 1,
            },
            {
                accessorKey: "PhoneNumber",
                header: "Phone Number",
                enableClickToCopy: true,
                size: 150,
                flex: 1,
            },
            {
                accessorKey: "DateOfBirth",
                header: "Date of Birth",
                enableClickToCopy: true,
                size: 150,
                flex: 1,
            },
        ],
        []
    );

    useEffect(() => {
        getStudents().then((data) => {
            setStudents(data);
            setIsUpdated(false);
        });
    }, [isUpdated]);

    const handleAddClick = () => {
        setCurrentStudent(null);
        setModalShow(true);
    };

    const handleEditClick = (student) => {
        setCurrentStudent(student);
        setModalShow(true);
    };

    const handleDeleteClick = (studentId) => {
        setStudentToDelete(studentId);
        setShowDeleteConfirm(true);
    };

    const confirmDelete = () => {
        deleteStudent(studentToDelete).then(
            (result) => {
                setIsUpdated(true);
                setTimeout(() => {
                    setShowDeleteConfirm(false);
                }, 500);
            },
            (error) => {
                alert("Failed to Delete Student");
                setShowDeleteConfirm(false);
            }
        );
    };

    const cancelDelete = () => {
        setShowDeleteConfirm(false);
        setStudentToDelete(null);
    };

    const modalClose = () => setModalShow(false);

    const handleAddSummaryClick = (student) => {
        setCurrentStudentForSummary(student);
        setShowSummaryModal(true);
    };

    const table = useMaterialReactTable({
        columns,
        data: students,
        enableColumnFilterModes: true,
        enableColumnOrdering: true,
        enableGrouping: false,
        enableColumnPinning: true,
        enableFacetedValues: true,
        enableRowActions: true,
        initialState: {
            showColumnFilters: false,
            showGlobalFilter: false,
            columnPinning: {
                left: ["mrt-row-expand", "mrt-row-select"],
                right: ["mrt-row-actions"],
            },
        },
        paginationDisplayMode: "pages",
        positionToolbarAlertBanner: "bottom",
        muiSearchTextFieldProps: {
            placeholder: "Search All Fields",
            size: "small",
            variant: "outlined",
        },
        muiPaginationProps: {
            color: "secondary",
            rowsPerPageOptions: [10, 20, 30],
            shape: "rounded",
            variant: "outlined",
        },

        // renderDetailPanel: ({ row }) => (
        //     <Box
        //         sx={{
        //             alignItems: "center",
        //             display: "flex",
        //             justifyContent: "space-around",
        //             left: "30px",
        //             maxWidth: "1000px",
        //             position: "sticky",
        //             width: "100%",
        //         }}
        //     >
        //         <Box sx={{ p: 2 }}>
        //             <Typography>
        //                 Registration No: {row.original.RegistrationNo}
        //             </Typography>
        //             <Typography>Course: {row.original.Course}</Typography>
        //         </Box>
        //     </Box>
        // ),
        renderRowActionMenuItems: ({ row, closeMenu }) => [
            <MenuItem
                key={0}
                onClick={() => {
                    handleEditClick(row.original);
                    closeMenu();
                }}
                sx={{ m: 0 }}
            >
                <ListItemIcon>
                    <Edit />
                </ListItemIcon>
                Edit Profile
            </MenuItem>,
            <MenuItem
                key={1}
                onClick={() => {
                    handleDeleteClick(row.original.studentId);
                    closeMenu();
                }}
                sx={{ m: 0 }}
            >
                <ListItemIcon>
                    <Delete />
                </ListItemIcon>
                Delete Client
            </MenuItem>,
            <MenuItem
                key={1}
                onClick={() => {
                    handleAddSummaryClick(row.original);
                    closeMenu();
                }}
                sx={{ m: 0 }}
            >
                <ListItemIcon>
                    <NoteAdd />
                </ListItemIcon>
                Create Summary
            </MenuItem>,
        ],
        renderTopToolbar: ({ table }) => {
            return (
                <Box
                    sx={(theme) => ({
                        backgroundColor: lighten(
                            theme.palette.background.default,
                            0.05
                        ),
                        display: "flex",
                        gap: "0.5rem",
                        p: "8px",
                        justifyContent: "space-between",
                    })}
                >
                    <Box
                        sx={{
                            display: "flex",
                            gap: "0.5rem",
                            alignItems: "center",
                        }}
                    >
                        <MRT_ToggleFiltersButton table={table} />
                    </Box>
                    <Box sx={{ display: "flex", gap: "0.5rem" }}>
                        <Button
                            color="primary"
                            onClick={handleAddClick}
                            variant="contained"
                        >
                            <i className="bi bi-person-fill-add"></i>

                            <span className="d-none d-sm-inline ms-2">
                                Add Client
                            </span>
                        </Button>
                    </Box>
                </Box>
            );
        },
    });

    return (
        <div>
            <MaterialReactTable table={table} />
            ;
            <StudentFormModal
                show={modalShow}
                onHide={modalClose}
                setUpdated={setIsUpdated}
                student={currentStudent}
                isUpdate={currentStudent != null}
            />
            <DeleteConfirmation
                show={showDeleteConfirm}
                onConfirm={confirmDelete}
                onCancel={cancelDelete}
            />
            <StudentSummaryFormModal
                show={showSummaryModal}
                setUpdated={setIsUpdated}
                onHide={() => setShowSummaryModal(false)}
                student={currentStudentForSummary}
            />
        </div>
    );
};

export default StudentList;
