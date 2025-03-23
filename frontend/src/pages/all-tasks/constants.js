import ActionsCellRenderer from '../../components/cell-renderers/ActionCellRenderer';
import DateTimeCellRenderer from '../../components/cell-renderers/DateTimeCellRenderer';
import { StatusCellRenderer } from '../../components/cell-renderers/StatusCellRenderer';
import TextCellRenderer from '../../components/cell-renderers/TextCellRenderer';
import { statusFormatter } from './utils';
export const allTaskColDef = [
    {
        field: 'TaskNumber',
        headerName: 'No.',
        width: 50,
        valueGetter: (params) => params.node.rowIndex + 1, // Auto-generate row number
    },
    {
        field: 'created_at',
        headerName: 'Created At',
        width: 100,
        autoHeight: true,
        wrapText: true,
        cellRenderer: DateTimeCellRenderer,
    },
    {
        field: 'query',
        headerNamer: 'Query',
        width: 200,
        cellRenderer: TextCellRenderer,
        autoHeight: true,
        wrapText: true,
    },
    {
        field: 'final_response',
        headerName: 'Response',
        width: 200,
        cellRenderer: TextCellRenderer,
        autoHeight: true,
        wrapText: true,
    },
    {
        field: 'status',
        headerName: 'Status',
        valueFormatter: statusFormatter,
        cellRenderer: StatusCellRenderer,
        filterParams: {
            valueFormatter: statusFormatter,
        },
        headerClass: 'header-status',
    },

    { field: 'actions', cellRenderer: ActionsCellRenderer },
];

export const paginationPageSizeSelector = [5, 10, 20];
