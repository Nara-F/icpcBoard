-- Native repeated headers, with cell conversion delegated to Pandoc's writer.
-- Works with the Table AST shared by Pandoc 3.x, without patching generated text.
function Table(tbl)
  local function cell(c)
    assert(c.row_span == 1 and c.col_span == 1, "Merged cells are not supported")
    return "[" .. pandoc.write(pandoc.Pandoc(c.contents), "typst") .. "]"
  end
  local function row(r)
    return table.concat(r.cells:map(cell), ",\n")
  end
  local aligns = {}
  for _, spec in ipairs(tbl.colspecs) do
    local a = tostring(spec[1])
    table.insert(aligns, a == "AlignRight" and "right" or a == "AlignCenter" and "center" or "left")
  end
  local parts = {
    "#board-table(columns: " .. #tbl.colspecs .. ", aligns: (" .. table.concat(aligns, ", ") .. ",),",
    "table.header(" .. table.concat(tbl.head.rows:map(row), ",\n") .. "),"
  }
  for _, body in ipairs(tbl.bodies) do
    for _, r in ipairs(body.head) do table.insert(parts, row(r) .. ",") end
    for _, r in ipairs(body.body) do table.insert(parts, row(r) .. ",") end
  end
  for _, r in ipairs(tbl.foot.rows) do table.insert(parts, row(r) .. ",") end
  table.insert(parts, ")")
  return pandoc.RawBlock("typst", table.concat(parts, "\n"))
end
