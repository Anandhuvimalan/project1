// ============================================================
// KERALA CAR DEALERSHIP - POWER QUERY M CODE
// ============================================================
// 
// HOW TO USE:
// 1. Open Power BI Desktop
// 2. Click "Get Data" → "Text/CSV"
// 3. Select: kerala_car_dealership_data.csv
// 4. Click "Transform Data" to open Power Query Editor
// 5. Go to Home → Advanced Editor
// 6. DELETE all existing code
// 7. PASTE this entire code
// 8. Click "Done"
// 9. Click "Close & Apply"
//
// ============================================================

let
    // Step 1: Load the CSV file
    Source = Csv.Document(
        File.Contents("C:\Users\anand\Desktop\project1\kerala_car_dealership_data.csv"),
        [Delimiter=",", Columns=37, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    
    // Step 2: Promote first row as headers
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    
    // Step 3: Set correct data types for all columns
    ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
        {"Transaction_ID", type text},
        {"Sale_Date", type date},
        {"Sale_Time", type time},
        {"Customer_Name", type text},
        {"Customer_Phone", type text},
        {"Customer_Email", type text},
        {"Customer_Address", type text},
        {"Customer_Age_Group", type text},
        {"Customer_Occupation", type text},
        {"Vehicle_Make", type text},
        {"Vehicle_Model", type text},
        {"Vehicle_Variant", type text},
        {"Manufacturing_Year", Int64.Type},
        {"Vehicle_Color", type text},
        {"Fuel_Type", type text},
        {"Transmission", type text},
        {"Condition", type text},
        {"Odometer_KM", Int64.Type},
        {"Chassis_Number", type text},
        {"Registration_Number", type text},
        {"Ex_Showroom_Price_INR", Currency.Type},
        {"Accessories_Cost_INR", Currency.Type},
        {"RTO_Charges_INR", Currency.Type},
        {"Insurance_Premium_INR", Currency.Type},
        {"Total_On_Road_Price_INR", Currency.Type},
        {"Payment_Method", type text},
        {"Down_Payment_INR", Currency.Type},
        {"Loan_Amount_INR", Currency.Type},
        {"Loan_Tenure_Months", Int64.Type},
        {"Interest_Rate_Percent", type number},
        {"Insurance_Type", type text},
        {"Warranty_Type", type text},
        {"Salesperson_Name", type text},
        {"Dealership_Branch", type text},
        {"District", type text},
        {"Test_Drive_Taken", type text},
        {"Referral_Source", type text}
    }),
    
    // Step 4: Add Sale_Year column
    AddedYear = Table.AddColumn(ChangedTypes, "Sale_Year", each Date.Year([Sale_Date]), Int64.Type),
    
    // Step 5: Add Sale_Month (month name)
    AddedMonthName = Table.AddColumn(AddedYear, "Sale_Month", each Date.MonthName([Sale_Date]), type text),
    
    // Step 6: Add Month_Number
    AddedMonthNumber = Table.AddColumn(AddedMonthName, "Month_Number", each Date.Month([Sale_Date]), Int64.Type),
    
    // Step 7: Add Quarter
    AddedQuarter = Table.AddColumn(AddedMonthNumber, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Sale_Date])), type text),
    
    // Step 8: Add Day_Name
    AddedDayName = Table.AddColumn(AddedQuarter, "Day_Name", each Date.DayOfWeekName([Sale_Date]), type text),
    
    // Step 9: Add Year_Month (for trend analysis)
    AddedYearMonth = Table.AddColumn(AddedDayName, "Year_Month", each Date.ToText([Sale_Date], "yyyy-MM"), type text),
    
    // Step 10: Add Vehicle_Age_Years
    AddedVehicleAge = Table.AddColumn(AddedYearMonth, "Vehicle_Age_Years", each Date.Year([Sale_Date]) - [Manufacturing_Year], Int64.Type),
    
    // Step 11: Add Price_Segment
    AddedPriceSegment = Table.AddColumn(AddedVehicleAge, "Price_Segment", each 
        if [Total_On_Road_Price_INR] < 600000 then "Budget (< ₹6L)"
        else if [Total_On_Road_Price_INR] < 1200000 then "Mid-Range (₹6L-12L)"
        else if [Total_On_Road_Price_INR] < 2000000 then "Premium (₹12L-20L)"
        else "Luxury (> ₹20L)", type text),
    
    // Step 12: Add Is_New_Car flag
    AddedIsNew = Table.AddColumn(AddedPriceSegment, "Is_New_Car", each if [Condition] = "New" then "Yes" else "No", type text),
    
    // Step 13: Add Loan_Taken flag
    AddedLoanFlag = Table.AddColumn(AddedIsNew, "Loan_Taken", each if [Loan_Amount_INR] > 0 then "Yes" else "No", type text),
    
    // Step 14: Add Profit_Margin estimate (approximate)
    AddedProfitMargin = Table.AddColumn(AddedLoanFlag, "Estimated_Margin_INR", each 
        if [Condition] = "New" then [Ex_Showroom_Price_INR] * 0.05
        else [Ex_Showroom_Price_INR] * 0.12, Currency.Type),
    
    // Step 15: Add Week_Number
    AddedWeekNumber = Table.AddColumn(AddedProfitMargin, "Week_Number", each Date.WeekOfYear([Sale_Date]), Int64.Type),
    
    // Step 16: Reorder columns for better organization
    ReorderedColumns = Table.ReorderColumns(AddedWeekNumber, {
        // Transaction Info
        "Transaction_ID", "Sale_Date", "Sale_Time", "Sale_Year", "Sale_Month", "Month_Number", 
        "Quarter", "Day_Name", "Year_Month", "Week_Number",
        // Customer Info
        "Customer_Name", "Customer_Phone", "Customer_Email", "Customer_Address", 
        "Customer_Age_Group", "Customer_Occupation",
        // Vehicle Info
        "Vehicle_Make", "Vehicle_Model", "Vehicle_Variant", "Manufacturing_Year", 
        "Vehicle_Age_Years", "Vehicle_Color", "Fuel_Type", "Transmission", 
        "Condition", "Is_New_Car", "Odometer_KM", "Chassis_Number", "Registration_Number",
        // Pricing
        "Ex_Showroom_Price_INR", "Accessories_Cost_INR", "RTO_Charges_INR", 
        "Insurance_Premium_INR", "Total_On_Road_Price_INR", "Price_Segment", "Estimated_Margin_INR",
        // Payment
        "Payment_Method", "Down_Payment_INR", "Loan_Amount_INR", "Loan_Taken",
        "Loan_Tenure_Months", "Interest_Rate_Percent",
        // Insurance & Warranty
        "Insurance_Type", "Warranty_Type",
        // Dealership
        "Salesperson_Name", "Dealership_Branch", "District",
        // Other
        "Test_Drive_Taken", "Referral_Source"
    })

in
    ReorderedColumns
