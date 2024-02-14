import React, { useMemo, useState, useEffect } from "react";
import {
    MaterialReactTable,
    useMaterialReactTable,
} from "material-react-table";
import { MenuItem, ListItemIcon } from "@mui/material";
import { RiDeleteBin5Line } from "react-icons/ri";
import { FaEdit, FaFilePdf } from "react-icons/fa";
import {
    getStudentSummaries,
    deleteStudentSummary,
} from "../services/StudentSummaryService";
import DeleteConfirmation from "./DeleteConfirmation";
import StudentSummaryFormModal from "./StudentSummaryFormModal";

const StudentSummaryList = () => {
    const [summaries, setSummaries] = useState([]);
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
    const [summaryToDelete, setSummaryToDelete] = useState(null);
    const [isUpdated, setIsUpdated] = useState(false);
    const [modalShow, setModalShow] = useState(false);
    const [currentSummary, setCurrentSummary] = useState(null);
    useEffect(() => {
        getStudentSummaries().then((data) => {
            setSummaries(data);
            setIsUpdated(false);
        });
    }, [isUpdated]);

    const handleDeleteClick = (summaryId) => {
        setSummaryToDelete(summaryId);
        setShowDeleteConfirm(true);
    };

    const confirmDelete = () => {
        deleteStudentSummary(summaryToDelete).then(
            (result) => {
                setIsUpdated(true);
                setTimeout(() => {
                    setShowDeleteConfirm(false);
                }, 500);
            },
            (error) => {
                alert("Failed to Delete Summary");
                setShowDeleteConfirm(false);
            }
        );
    };

    const cancelDelete = () => {
        setShowDeleteConfirm(false);
        setSummaryToDelete(null);
    };

    const handleEditClick = (summary) => {
        setCurrentSummary(summary);
        setModalShow(true);
    };

    const modalClose = () => setModalShow(false);

    const tableStyle = {
        "& .MuiTableCell-root": {
            fontSize: { xs: "0.75rem", sm: "0.875rem" },
            padding: { xs: "6px", sm: "16px" },
            "& .MuiTableCell-head": {
                fontSize: { xs: "0.25rem", sm: "0.875rem" },
            },
        },
    };

    const columns = useMemo(
        () => [
            {
                accessorKey: "student.FirstName", // accessor is the "key" in the data
                header: "First Name",
            },
            {
                accessorKey: "student.LastName",
                header: "Last Name",
            },
            {
                accessorKey: "date_created",
                header: "Date Created",
                Cell: ({ cell }) =>
                    new Date(cell.getValue()).toLocaleDateString(),
            },
        ],
        []
    );

    const tableInstance = useMaterialReactTable({
        columns,
        data: summaries,
        enableColumnFilterModes: true,
        enableColumnOrdering: true,
        enableGrouping: true,
        enableColumnPinning: true,
        enableFacetedValues: true,
        enableRowActions: true,
        initialState: {
            showColumnFilters: false,
            showGlobalFilter: true,
            columnPinning: {
                left: ["mrt-row-expand", "mrt-row-select"],
                right: ["mrt-row-actions"],
            },
        },
        paginationDisplayMode: "pages",
        positionToolbarAlertBanner: "bottom",
        muiSearchTextFieldProps: {
            size: "small",
            variant: "outlined",
        },
        muiPaginationProps: {
            color: "secondary",
            rowsPerPageOptions: [10, 20, 30],
            shape: "rounded",
            variant: "outlined",
        },
        muiTableContainerProps: {
            sx: {
                "& .MuiTableCell-root": {
                    fontSize: { xs: "0.75rem", sm: "0.875rem" },
                },
                overflowX: "auto",
            },
        },

        renderRowActionMenuItems: ({ row, closeMenu }) => [
            <MenuItem
                key="edit"
                onClick={() => {
                    closeMenu();
                    handleEditClick(row.original);
                }}
            >
                <ListItemIcon>
                    <FaEdit />
                </ListItemIcon>
                Edit
            </MenuItem>,
            <MenuItem
                key="delete"
                onClick={() => {
                    closeMenu();
                    handleDeleteClick(row.original.id);
                }}
            >
                <ListItemIcon>
                    <RiDeleteBin5Line />
                </ListItemIcon>
                Delete
            </MenuItem>,
            <MenuItem
                key="download"
                component="a"
                href={row.original.pdf_file}
                target="_blank"
                rel="noopener noreferrer"
                onClick={() => {
                    closeMenu();
                }}
            >
                <ListItemIcon>
                    <FaFilePdf />
                </ListItemIcon>
                Download PDF
            </MenuItem>,
        ],
    });

    return (
        <div>
            <div style={{ display: "grid" }}>
                {" "}
                <MaterialReactTable table={tableInstance} sx={tableStyle} />
            </div>

            <DeleteConfirmation
                show={showDeleteConfirm}
                onConfirm={confirmDelete}
                onCancel={cancelDelete}
            />

            <StudentSummaryFormModal
                show={modalShow}
                onHide={modalClose}
                summary={currentSummary}
                setUpdated={setIsUpdated}
                isUpdate={currentSummary != null}
            />
        </div>
    );
};

export default StudentSummaryList;
