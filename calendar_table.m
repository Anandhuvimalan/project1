// ============================================================
// CALENDAR/DATE TABLE - POWER QUERY M CODE
// ============================================================
// 
// HOW TO USE:
// 1. In Power Query Editor, click Home → New Source → Blank Query
// 2. Click "Advanced Editor"
// 3. DELETE all existing code
// 4. PASTE this entire code
// 5. Click "Done"
// 6. In Query Settings (right side), rename to "Calendar"
// 7. Click "Close & Apply"
//
// AFTER LOADING:
// 1. Go to Model View in Power BI
// 2. Drag Calendar[Date] to Sales_Transactions[Sale_Date] to create relationship
// 3. Go to Table Tools → Mark as Date Table → Select "Date" column
//
// ============================================================

let
    // Define date range (matches your sales data range)
    StartDate = #date(2022, 1, 1),
    EndDate = #date(2026, 12, 31),
    
    // Calculate number of days
    NumberOfDays = Duration.Days(EndDate - StartDate) + 1,
    
    // Create list of dates
    DateList = List.Dates(StartDate, NumberOfDays, #duration(1, 0, 0, 0)),
    
    // Convert to table
    DateTable = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),
    
    // Set Date column type
    ChangedType = Table.TransformColumnTypes(DateTable, {{"Date", type date}}),
    
    // Add Year
    AddedYear = Table.AddColumn(ChangedType, "Year", each Date.Year([Date]), Int64.Type),
    
    // Add Month Number
    AddedMonthNum = Table.AddColumn(AddedYear, "Month_Number", each Date.Month([Date]), Int64.Type),
    
    // Add Month Name
    AddedMonthName = Table.AddColumn(AddedMonthNum, "Month_Name", each Date.MonthName([Date]), type text),
    
    // Add Month Short (Jan, Feb, etc.)
    AddedMonthShort = Table.AddColumn(AddedMonthName, "Month_Short", each Text.Start(Date.MonthName([Date]), 3), type text),
    
    // Add Quarter
    AddedQuarter = Table.AddColumn(AddedMonthShort, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    
    // Add Quarter Number
    AddedQuarterNum = Table.AddColumn(AddedQuarter, "Quarter_Number", each Date.QuarterOfYear([Date]), Int64.Type),
    
    // Add Day of Month
    AddedDay = Table.AddColumn(AddedQuarterNum, "Day", each Date.Day([Date]), Int64.Type),
    
    // Add Day Name
    AddedDayName = Table.AddColumn(AddedDay, "Day_Name", each Date.DayOfWeekName([Date]), type text),
    
    // Add Day Short (Mon, Tue, etc.)
    AddedDayShort = Table.AddColumn(AddedDayName, "Day_Short", each Text.Start(Date.DayOfWeekName([Date]), 3), type text),
    
    // Add Day of Week Number (1 = Sunday, 7 = Saturday)
    AddedDayOfWeek = Table.AddColumn(AddedDayShort, "Day_of_Week", each Date.DayOfWeek([Date], Day.Sunday) + 1, Int64.Type),
    
    // Add Week Number
    AddedWeekNum = Table.AddColumn(AddedDayOfWeek, "Week_Number", each Date.WeekOfYear([Date]), Int64.Type),
    
    // Add Year-Month (for sorting trends)
    AddedYearMonth = Table.AddColumn(AddedWeekNum, "Year_Month", each Date.ToText([Date], "yyyy-MM"), type text),
    
    // Add Year-Quarter
    AddedYearQuarter = Table.AddColumn(AddedYearMonth, "Year_Quarter", each Text.From(Date.Year([Date])) & "-Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    
    // Add Is Weekend
    AddedIsWeekend = Table.AddColumn(AddedYearQuarter, "Is_Weekend", each if Date.DayOfWeek([Date], Day.Monday) >= 5 then "Yes" else "No", type text),
    
    // Add Fiscal Year (April to March in India)
    AddedFiscalYear = Table.AddColumn(AddedIsWeekend, "Fiscal_Year", each 
        if Date.Month([Date]) >= 4 then "FY " & Text.From(Date.Year([Date])) & "-" & Text.End(Text.From(Date.Year([Date]) + 1), 2)
        else "FY " & Text.From(Date.Year([Date]) - 1) & "-" & Text.End(Text.From(Date.Year([Date])), 2), type text),
    
    // Add Fiscal Quarter
    AddedFiscalQuarter = Table.AddColumn(AddedFiscalYear, "Fiscal_Quarter", each 
        let month = Date.Month([Date]) in
        if month >= 4 and month <= 6 then "FQ1"
        else if month >= 7 and month <= 9 then "FQ2"
        else if month >= 10 and month <= 12 then "FQ3"
        else "FQ4", type text),
    
    // Add Month-Year (for display)
    AddedMonthYear = Table.AddColumn(AddedFiscalQuarter, "Month_Year", each Date.ToText([Date], "MMM yyyy"), type text),
    
    // Sort Month Name by Month Number
    SortedMonthName = Table.Sort(AddedMonthYear, {{"Date", Order.Ascending}})

in
    SortedMonthName
