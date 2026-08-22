import React from 'react'
import { flexRender, getCoreRowModel, getPaginationRowModel, getSortedRowModel, useReactTable } from '@tanstack/react-table'
import { ChevronDown, ChevronUp, ChevronsUpDown } from 'lucide-react'

function DataTable({ columns, rows, emptyMessage = 'No data found.', onRowClick }) {
  const table = useReactTable({
    data: rows,
    columns: columns.map((column) => ({
      accessorKey: column.key,
      id: column.key,
      header: column.label,
      enableSorting: column.sortable !== false,
      cell: column.render ? ({ row }) => column.render(row.original) : ({ getValue }) => getValue() ?? '',
    })),
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: { pagination: { pageSize: 8 } },
  })

  return (
    <div>
      <div className="table-wrap">
        <table className="data-table">
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th key={header.id}>
                  {header.isPlaceholder ? null : (
                    <button type="button" className="table-sort-button" onClick={header.column.getToggleSortingHandler()} disabled={!header.column.getCanSort()}>
                      {flexRender(header.column.columnDef.header, header.getContext())}
                      {header.column.getCanSort() ? (header.column.getIsSorted() === 'asc' ? <ChevronUp size={14} /> : header.column.getIsSorted() === 'desc' ? <ChevronDown size={14} /> : <ChevronsUpDown size={14} />) : null}
                    </button>
                  )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.length > 0 ? (
            table.getRowModel().rows.map((row) => (
              <tr key={row.id} className={onRowClick ? 'clickable-row' : ''} onClick={() => onRowClick?.(row.original)}>
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</td>
                ))}
              </tr>
            ))
          ) : (
            <tr>
              <td className="empty-cell" colSpan={table.getAllColumns().length}>
                {emptyMessage}
              </td>
            </tr>
          )}
        </tbody>
        </table>
      </div>
      {rows.length > 0 ? (
        <div className="table-pagination">
          <span>Page {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}</span>
          <div className="pagination-actions">
            <button type="button" className="secondary-button small" onClick={() => table.previousPage()} disabled={!table.getCanPreviousPage()}>Previous</button>
            <button type="button" className="secondary-button small" onClick={() => table.nextPage()} disabled={!table.getCanNextPage()}>Next</button>
          </div>
        </div>
      ) : null}
    </div>
  )
}

export default DataTable
