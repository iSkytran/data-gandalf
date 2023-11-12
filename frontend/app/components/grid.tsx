import ReactPaginate from "react-paginate";

export default function Grid({
  pageCount,
  pageChange,
  children,
}: {
  pageCount?: number;
  pageChange?: any;
  children?: Array<React.ReactNode>;
}) {
  const paginateStyle =
    "flex items-center justify-center leading-tight text-white p-2 hover:bg-medium_blue";
  const paginateItem = pageCount && pageChange && (
    <ReactPaginate
      className="inline-flex my-4"
      activeLinkClassName={`${paginateStyle} !bg-light_blue !text-sas_blue`}
      previousLinkClassName={`${paginateStyle} rounded-l-lg bg-sas_blue`}
      nextLinkClassName={`${paginateStyle} rounded-r-lg bg-sas_blue`}
      pageLinkClassName={`${paginateStyle} bg-sas_blue`}
      breakLinkClassName={`${paginateStyle} bg-sas_blue`}
      pageCount={pageCount}
      onPageChange={pageChange}
      renderOnZeroPageCount={null}
    />
  );

  return (
    <>
      {paginateItem}
      <div className="w-full grid grid-cols-2 gap-4">{children}</div>
      {paginateItem}
    </>
  );
}
