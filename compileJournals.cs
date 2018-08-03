// https://code.msdn.microsoft.com/windowsapps/Utilizzo-della-libreria-77c28353
//dll net framework 
using System; 
using System.Linq; 
using System.Windows.Forms; 
 
//NameSpace ClosedXlmSample 
namespace ClosedXmlSample 
{ 
    //FrmClosedXml Class 
    public partial class FrmClosedXmlSample : Form 
    { 
        /*I declare a variable of type bool, this variable is handled when the user 
         *select a row in the DataGrid control to allow you to erase and edit data*/ 
        private bool _checkifrowisselected ; 
         
        // Constructor of the class FrmClosedXmlSample 
        public FrmClosedXmlSample() 
        { 
            //InitializeComponent Method 
            InitializeComponent(); 
        } 
 
        //FrmClosedXmlSampleLoad Event 
        private void FrmClosedXmlSampleLoad(object sender, EventArgs e) 
        { 
            /*This method loads the data into the control using the TableAdapter's Fill method,  
            and then the DataGridView control is enhanced with the original data using the DataSource property*/ 
            LoadDataGrid(); 
        } 
 
        //BtnNewClick Event 
        private void BtnNewClick(object sender, EventArgs e) 
        { 
            /*Insert this method does nothing but make the exploitation of fields of DataTable after inserting a new record into the table UserData*/ 
            uSERDATATableAdapter.Insert(txtName.Text.ToUpper(), txtSurname.Text.ToUpper(), txtAddress.Text.ToUpper(), txtTelephoneNumber.Text.ToUpper(), 
                                        txtCity.Text.ToUpper(), txtNationality.Text.ToUpper()); 
             
            /*This method loads the data into the control using the TableAdapter's Fill method,  
            and then the DataGridView control is enhanced with the original data using the DataSource property*/ 
            LoadDataGrid(); 
        } 
 
        //BtnDeleteClick Event 
        private void BtnDeleteClick(object sender, EventArgs e) 
        { 
            /*If not _checkifrowisselected equals false*/ 
            if(!_checkifrowisselected.Equals(false)) 
            { 
                /*check if current row is not null*/ 
                if (dgvUserData.CurrentRow == null) return; 
 
                /*Delete this method does is erase the fields in the UserData table, execute the passing as argument the number of records that we select using the DataGridView control,  
                 *before removal of the record, it checks to see if the user has selected or least one row of the DataGridView control*/ 
                uSERDATATableAdapter.Delete(int.Parse(dgvUserData.CurrentRow.Cells[0].Value.ToString())); 
 
                /*This method loads the data into the control using the TableAdapter's Fill method,  
                and then the DataGridView control is enhanced with the original data using the DataSource property*/ 
                LoadDataGrid(); 
 
                /*set to false variable*/ 
                _checkifrowisselected = false; 
            } 
 
            else 
            { 
                /*Visualize message to user*/ 
                MessageBox.Show(Properties.Resources.FrmClosedXmlSample_BtnDeleteClick_Select_one_row); 
            } 
        } 
 
        //BtnUpdate Event 
        private void BtnUpdateClick(object sender, EventArgs e) 
        { 
            /*If not _checkifrowisselected equals false*/ 
            if (!_checkifrowisselected.Equals(false)) 
            { 
 
                /*Check if currentrow of DataGric is not null*/ 
                if (dgvUserData.CurrentRow == null) return; 
 
                uSERDATATableAdapter.Update(txtName.Text.ToUpper(), txtSurname.Text.ToUpper(), txtAddress.Text.ToUpper(), 
                                            txtTelephoneNumber.Text.ToUpper(), 
                                            txtCity.Text.ToUpper(), txtNationality.Text.ToUpper(), 
                                            int.Parse(dgvUserData.CurrentRow.Cells[0].Value.ToString())); 
 
                /*This method loads the data into the control using the TableAdapter's Fill method,  
                    and then the DataGridView control is enhanced with the original data using the DataSource property*/ 
                LoadDataGrid(); 
 
                /*set to false variable*/ 
                _checkifrowisselected = false; 
            } 
 
            else 
            { 
                /*Visualize message to user*/ 
                MessageBox.Show(Properties.Resources.FrmClosedXmlSample_BtnDeleteClick_Select_one_row); 
            } 
        } 
 
        //BtnReportClick Event 
        private void BtnReportClick(object sender, EventArgs e) 
        { 
            /*I declare a new instance of the Form Frmeport*/ 
            var frm = new FrmReport {DataReport = dgvUserData}; 
            /*I'm seeing the Forms user*/ 
            frm.Show(); 
        } 
 
        //BtnExitClick Event 
        private void BtnExitClick(object sender, EventArgs e) 
        { 
            //Close the application and Exit 
            Close(); 
        } 
 
        //BtnFindClick Event 
        private void BtnFindClick(object sender, EventArgs e) 
        { 
            /*I get the currently selected text to the ComboBox control*/ 
            var selecteditems = cbxFind.Text; 
 
            /*Executing the control of the variable SelectedItems with a Switch construct*/ 
            switch(selecteditems) 
            { 
                /*If SelectedItems equals NAME*/ 
                case "NAME": 
                    /*I run a query LinqToDataSet with extension method and recover all data from the UserData table and visualize the DataGrid control*/ 
                    var queryname = 
                        userDataSet.USERDATA.Where(w => w.NAME.StartsWith(txtName.Text.ToUpper())).Select( 
                            s => new {s.NAME, s.SURNAME, s.ADDRESS, s.TELEPHONE, s.CITY, s.NATIONALITI}).OrderBy(o=> o.NAME); 
                    dgvUserData.DataSource = queryname.ToArray(); 
                    /*Exit switch*/ 
                    break; 
 
                /*If SelectedItems equals CITY*/ 
                case "CITY": 
                    /*I run a query LinqToDataSet with extension method and recover all data from the UserData table and visualize the DataGrid control*/ 
                    var querycity = 
                        userDataSet.USERDATA.Where(w=> w.CITY.StartsWith(txtCity.Text.ToUpper())).Select( 
                            s => new { s.NAME, s.SURNAME, s.ADDRESS, s.TELEPHONE, s.CITY, s.NATIONALITI }).OrderBy(o => o.CITY); 
                    dgvUserData.DataSource = querycity.ToArray(); 
                    /*Exit switch*/ 
                    break; 
 
                /*If SelectedItems equals NATIONALITY*/ 
                case "NATIONALITY": 
                    /*I run a query LinqToDataSet with extension method and recover all data from the UserData table and visualize the DataGrid control*/ 
                    var querynationality = 
                        userDataSet.USERDATA.Where(w => w.NATIONALITI.StartsWith(txtNationality.Text.ToUpper())).Select( 
                            s => new { s.NAME, s.SURNAME, s.ADDRESS, s.TELEPHONE, s.CITY, s.NATIONALITI }).OrderBy(o => o.NATIONALITI); 
                    dgvUserData.DataSource = querynationality.ToArray(); 
                    /*Exit switch*/ 
                    break; 
            } 
        } 
 
        /*LoadDataGrid Method*/ 
        private void LoadDataGrid() 
        { 
            /*Load the data into the control TableAdapter*/ 
            uSERDATATableAdapter.Fill(userDataSet.USERDATA); 
            /*Load data with the DataGrid control*/ 
            dgvUserData.DataSource = uSERDATABindingSource; 
        } 
 
        /*CbxFindSelectedIndexChanged Event*/ 
        private void CbxFindSelectedIndexChanged(object sender, EventArgs e) 
        { 
            /*I get the currently selected text to the ComboBox control*/ 
            var selecteditems = cbxFind.Text; 
 
            /*Using a query LinqToObjects reimposed the Enabled property to true for all the text boxes on the form*/ 
            Controls.OfType<TextBox>().ToList().ForEach(f => f.Enabled = true); 
 
            /*Executing the control of the variable SelectedItems with a Switch construct*/ 
            switch (selecteditems) 
            { 
                /*If SelectedItems equals NAME*/ 
                case "NAME": 
                    /*I run a query LinqToDataSet with extension method and recover all data from the UserData table and visualize the DataGrid control*/ 
                    var queryname = 
                        userDataSet.USERDATA.Where(w => w.NAME.StartsWith(txtName.Text.ToUpper())).Select( 
                            s => new { s.NAME, s.SURNAME, s.ADDRESS, s.TELEPHONE, s.CITY, s.NATIONALITI }).OrderBy(o => o.NAME); 
                    dgvUserData.DataSource = queryname.ToArray(); 
                    /*Exit switch*/ 
                    break; 
 
                /*If SelectedItems equals SURNAME*/ 
                case "SURNAME": 
                    /*I run a query LinqToDataSet with extension method and recover all data from the UserData table and visualize the DataGrid control*/ 
                    Controls.OfType<TextBox>().Where(w => !w.Name.Equals("txtSurname")).ToList().ForEach( 
                        f => f.Enabled = false); 
                    /*Exit switch*/ 
                    break; 
 
                /*If SelectedItems equals ADDRESS*/ 
                case "ADDRESS": 
                    /*I run a query LinqToDataSet with extension method and recover all data from the UserData table and visualize the DataGrid control*/ 
                    Controls.OfType<TextBox>().Where(w => !w.Name.Equals("txtAddress")).ToList().ForEach( 
                        f => f.Enabled = false); 
                    /*Exit switch*/ 
                    break; 
 
                /**/ 
                case "TELEPHONE NUMBER": 
                    /**/ 
                    Controls.OfType<TextBox>().Where(w => !w.Name.Equals("txtTelephoneNumber")).ToList().ForEach( 
                        f => f.Enabled = false); 
                    /**/ 
                    break; 
 
                /*If SelectedItems equals CITY*/ 
                case "CITY": 
                    /*I run a query LinqToDataSet with extension method and recover all data from the UserData table and visualize the DataGrid control*/ 
                    var querycity = 
                        userDataSet.USERDATA.Where(w => w.CITY.StartsWith(txtCity.Text.ToUpper())).Select( 
                            s => new { s.NAME, s.SURNAME, s.ADDRESS, s.TELEPHONE, s.CITY, s.NATIONALITI }).OrderBy(o => o.CITY); 
                    dgvUserData.DataSource = querycity.ToArray(); 
                    /*Exit switch*/ 
                    break; 
 
                /*If SelectedItems equals NATIONALITY*/ 
                case "NATIONALITY": 
                    /*I run a query LinqToDataSet with extension method and recover all data from the UserData table and visualize the DataGrid control*/ 
                    var querynationality = 
                        userDataSet.USERDATA.Where(w => w.NATIONALITI.StartsWith(txtNationality.Text.ToUpper())).Select( 
                            s => new { s.NAME, s.SURNAME, s.ADDRESS, s.TELEPHONE, s.CITY, s.NATIONALITI }).OrderBy(o => o.NATIONALITI); 
                    dgvUserData.DataSource = querynationality.ToArray(); 
                    /*Exit switch*/ 
                    break; 
            } 
        } 
 
        //DgvUserDataRowHeaderMouseClick Event 
        private void DgvUserDataRowHeaderMouseClick(object sender, DataGridViewCellMouseEventArgs e) 
        { 
            /*set the variable to true */ 
            _checkifrowisselected = true; 
        } 
    } 
} 
////////////////////////
//dll net framework  
using System;  
using System.Globalization;  
using System.Windows.Forms;  
using ClosedXmlSample.Properties;  
  
//This and instead the reference that must be included in the project to use the library ClosedXml  
using ClosedXML.Excel;  
  
//NameSpace ClosedXlmSample  
namespace ClosedXmlSample  
{  
    //FrmReport Class  
    public partial class FrmReport : Form  
    {  
        // Constructor of the class FrmReport  
        public FrmReport()  
        {  
            //InitializeComponent Method  
            InitializeComponent();  
        }  
  
        //This property is value in the main form with the values ​​in the DataGrid, which then in turn enhances the Forms DataGrid control FrmReport  
        public DataGridView DataReport { get; set; }  
  
        //FrmReportLoad Event  
        private void FrmReportLoad(object sender, EventArgs e)  
        {  
            /*Enhanced the value control DataGrid using the property DataReport*/  
            dgvReport.DataSource = DataReport.DataSource;  
        }  
  
        //BtnExportToExcelClick Event  
        private void BtnExportToExcelClick(object sender, EventArgs e)  
        {  
            /*If the DataGrid control does not contain any column*/  
            if (dgvReport.Columns.Count.Equals(0))  
            {  
                /*I get a message to the user*/  
                MessageBox.Show(Resources.FrmReport_BtnSalvaInExcelClick_Nessuna_riga_da_salvare, Application.ProductName.ToString(CultureInfo.InvariantCulture));  
                return;  
            }  
  
            /*Imposed on the size of the file to be saved for the SaveFileDialog component,   
             * the format and saved in the application's resources.*/  
            sfDialog.Filter = Resources.FileXlsx;  
  
            /*Given the name of the excel file that will be generated.*/  
            sfDialog.FileName = "USER DATA";  
  
            /*Here, however, we create a new worksheet excel*/  
            var workbook = new XLWorkbook();  
  
            /*On the worksheet, create the worksheet in another sheet named user reports,   
             * this leaflet will be included in the excel file which will then be generated.*/  
            var worksheet = workbook.Worksheets.Add("USER DATA REPORT");  
  
            /*I create variables as there are columns of excel file to be created,   
             * in this case 6 and the imposed with a default value*/  
            var cellA = "A";  
            var cellB = "B";  
            var cellC = "C";  
            var cellD = "D";  
            var cellE = "E";  
            var cellF = "F";  
  
            /*This variable is used for the process of writing the various sections of the paper, the header,   
             * the name of the columns to end up with the values ​​of the DataGrid control*/  
            var indexcell = 0;  
  
            /*In this loop we perform the control of the variable index and it will create the header of the sheet,   
             * a title and the formatting of cells on the alignment of the title text*/  
            for (var riga = 0; riga < 4; riga++)  
            {  
                /*In this loop are enclosed in stages to the header in the title, the cell formatting and the column headings*/  
                indexcell += 1;  
  
                /*If index equals 1*/  
                if (indexcell.Equals(1))  
                {  
                    /*Allowance for cells and and the numerical value given by the variable i and indexcell*/  
                    cellA += indexcell.ToString(CultureInfo.InvariantCulture);  
                    cellF += indexcell.ToString(CultureInfo.InvariantCulture);  
  
                    /*The Merge method allows to combine two or more cells, in this case we combine the cells from a to f*/  
                    worksheet.Range(cellA + ":" + cellF).Merge();  
  
                    /*Assign a value to the cell, so that it can fill the contents of the cells to f*/  
                    worksheet.Cell(cellA).Value = "USER DATA";  
  
                    /*Check by enumeration XLAlignmentHorizontalValues​​, the alignment of text within the cell to be shown at the center*/  
                    worksheet.Cell(cellA).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;  
                    worksheet.Cell(cellA).Style.Fill.BackgroundColor = XLColor.CornflowerBlue;  
  
                    /*default value for cell a and f*/  
                    cellA = "A";  
                    cellF = "F";  
                }  
  
                /*If index equals 2*/  
                if (indexcell.Equals(2))  
                {  
                    /*Allowance for cells and and the numerical value given by the variable i and indexcell*/  
                    cellA += indexcell.ToString(CultureInfo.InvariantCulture);  
                    cellB += indexcell.ToString(CultureInfo.InvariantCulture);  
                    cellC += indexcell.ToString(CultureInfo.InvariantCulture);  
                    cellD += indexcell.ToString(CultureInfo.InvariantCulture);  
                    cellE += indexcell.ToString(CultureInfo.InvariantCulture);  
                    cellF += indexcell.ToString(CultureInfo.InvariantCulture);  
  
                    /*Here, however, we assign the cell to the cell f the name of the columns of the DataGrid control by property Value*/  
                    worksheet.Cell(cellA).Value = dgvReport.Columns[1].Name;  
                    worksheet.Cell(cellB).Value = dgvReport.Columns[2].Name;  
                    worksheet.Cell(cellC).Value = dgvReport.Columns[3].Name;  
                    worksheet.Cell(cellD).Value = dgvReport.Columns[4].Name;  
                    worksheet.Cell(cellE).Value = dgvReport.Columns[5].Name;  
                    worksheet.Cell(cellF).Value = dgvReport.Columns[6].Name;  
  
                    /*Check by enumeration XLAlignmentHorizontalValues​​, the alignment of text within the cell to be shown at the center*/  
                    worksheet.Cell(cellA).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;  
                    worksheet.Cell(cellB).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;  
                    worksheet.Cell(cellC).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;  
                    worksheet.Cell(cellD).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;  
                    worksheet.Cell(cellE).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;  
                    worksheet.Cell(cellF).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;  
  
                    /*default value for cell from a to f*/  
                    cellA = "A";  
                    cellB = "B";  
                    cellC = "C";  
                    cellD = "D";  
                    cellE = "E";  
                    cellF = "F";  
                }  
            }  
  
            /*In this loop will perform the control of the variable index and prodcederà to the writing of the values ​​contained in   
             * the DataGrid on the variables from cell to celfl, so pore actually write on the cells of the sheet excel*/  
            for (var riga = 0; riga < dgvReport.Rows.Count; riga++)  
            {  
                /*If index equals 3*/  
                if (indexcell > 3)  
                {  
                    /*Allowance for cells and and the numerical value given by the variable i and indexcell*/  
                    cellA += indexcell.ToString(CultureInfo.InvariantCulture);  
                    cellB += indexcell.ToString(CultureInfo.InvariantCulture);  
                    cellC += indexcell.ToString(CultureInfo.InvariantCulture);  
                    cellD += indexcell.ToString(CultureInfo.InvariantCulture);  
                    cellE += indexcell.ToString(CultureInfo.InvariantCulture);  
                    cellF += indexcell.ToString(CultureInfo.InvariantCulture);  
  
                    /*Here instead we assign from cell to cell f the value of each row in the DataGrid control and always through their Value property*/  
                    worksheet.Cell(cellA).Value = dgvReport.Rows[riga].Cells[1].Value;  
                    worksheet.Cell(cellB).Value = dgvReport.Rows[riga].Cells[2].Value;  
                    worksheet.Cell(cellC).Value = dgvReport.Rows[riga].Cells[3].Value;  
                    worksheet.Cell(cellD).Value = dgvReport.Rows[riga].Cells[4].Value;  
                    worksheet.Cell(cellE).Value = dgvReport.Rows[riga].Cells[5].Value;  
                    worksheet.Cell(cellF).Value = dgvReport.Rows[riga].Cells[6].Value;  
  
                    /*Check by enumeration XLAlignmentHorizontalValues​​, the alignment of text within the cell to be shown at the center*/  
                    worksheet.Cell(cellA).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;  
                    worksheet.Cell(cellB).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;  
                    worksheet.Cell(cellC).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;  
                    worksheet.Cell(cellD).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;  
                    worksheet.Cell(cellE).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;  
                    worksheet.Cell(cellF).Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;  
  
                    /*This method allows to adapt the text within the cells so that it is well centered and adapted to their inner*/  
                    worksheet.Columns().AdjustToContents();  
  
                    /*default value for cell from a to f*/  
                    cellA = "A";  
                    cellB = "B";  
                    cellC = "C";  
                    cellD = "D";  
                    cellE = "E";  
                    cellF = "F";  
                }  
  
                /*increase the value of the variable indexcell*/  
                indexcell += 1;  
            }  
  
            /*Here we give the user the possibility scegiere where to save the file which will then be generated using the SaveFileDialog*/  
            if (sfDialog.ShowDialog().Equals(DialogResult.OK))  
            {  
                /*This method will save the file in xlsx excel where the user decide this   
                 * by the argument required by that method where we spend the path of destination*/  
                workbook.SaveAs(sfDialog.FileName);  
            }  
        }  
  
        //BtnExitClick Event  
        private void BtnExitClick(object sender, EventArgs e)  
        {  
            /*Close actual Form*/  
            Close();  
        }  
    }  
} 
