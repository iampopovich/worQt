/*
 * Создано в SharpDevelop.
 * Пользователь: PopovAV
 * Дата: 11.12.2018
 * Время: 18:09
 * 
 * Для изменения этого шаблона используйте меню "Инструменты | Параметры | Кодирование | Стандартные заголовки".
 */
namespace techReqs
{
	partial class MainForm
	{
		/// <summary>
		/// Designer variable used to keep track of non-visual components.
		/// </summary>
		//private System.ComponentModel.IContainer components = null;
		private System.Windows.Forms.ListBox leftListbox;
		private System.Windows.Forms.ListBox midListbox;
		private System.Windows.Forms.TextBox midTexbox;
		private System.Windows.Forms.ListBox rightListbox;
		private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
		private System.Windows.Forms.Button button1;
		private System.Windows.Forms.Button button2;
		private System.Windows.Forms.CheckBox checkBox1;
		private System.Windows.Forms.Button button3;
		
		private void InitializeComponent()
		{
			this.leftListbox = new System.Windows.Forms.ListBox();
			this.midListbox = new System.Windows.Forms.ListBox();
			this.midTexbox = new System.Windows.Forms.TextBox();
			this.rightListbox = new System.Windows.Forms.ListBox();
			this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
			this.button1 = new System.Windows.Forms.Button();
			this.button2 = new System.Windows.Forms.Button();
			this.checkBox1 = new System.Windows.Forms.CheckBox();
			this.button3 = new System.Windows.Forms.Button();
			this.tableLayoutPanel1.SuspendLayout();
			this.SuspendLayout();
			// 
			// leftListbox
			// 
			this.leftListbox.FormattingEnabled = true;
			this.leftListbox.Items.AddRange(new object[] {
			"test"});
			this.leftListbox.Location = new System.Drawing.Point(12, 25);
			this.leftListbox.Name = "leftListbox";
			this.leftListbox.Size = new System.Drawing.Size(260, 407);
			this.leftListbox.TabIndex = 0;
			this.leftListbox.SelectedIndexChanged += new System.EventHandler(this.LeftListboxSelectedIndexChanged);
			// 
			// midListbox
			// 
			this.midListbox.FormattingEnabled = true;
			this.midListbox.Location = new System.Drawing.Point(278, 298);
			this.midListbox.Name = "midListbox";
			this.midListbox.Size = new System.Drawing.Size(392, 134);
			this.midListbox.TabIndex = 1;
			// 
			// midTexbox
			// 
			this.midTexbox.Location = new System.Drawing.Point(278, 25);
			this.midTexbox.Multiline = true;
			this.midTexbox.Name = "midTexbox";
			this.midTexbox.Size = new System.Drawing.Size(392, 229);
			this.midTexbox.TabIndex = 2;
			// 
			// rightListbox
			// 
			this.rightListbox.DrawMode = System.Windows.Forms.DrawMode.OwnerDrawVariable;
			this.rightListbox.FormattingEnabled = true;
			this.rightListbox.Location = new System.Drawing.Point(676, 25);
			this.rightListbox.Name = "rightListbox";
			this.rightListbox.SelectionMode = System.Windows.Forms.SelectionMode.MultiExtended;
			this.rightListbox.Size = new System.Drawing.Size(548, 407);
			this.rightListbox.TabIndex = 3;
			this.rightListbox.DrawItem += new System.Windows.Forms.DrawItemEventHandler(this.RightListboxDrawItem);
			this.rightListbox.MeasureItem += new System.Windows.Forms.MeasureItemEventHandler(this.RightListboxMeasureItem);
			this.rightListbox.DoubleClick += new System.EventHandler(this.editCurrentLine);
			// 
			// tableLayoutPanel1
			// 
			this.tableLayoutPanel1.BackgroundImageLayout = System.Windows.Forms.ImageLayout.None;
			this.tableLayoutPanel1.ColumnCount = 3;
			this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.33333F));
			this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.33333F));
			this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33.33333F));
			this.tableLayoutPanel1.Controls.Add(this.button1, 0, 0);
			this.tableLayoutPanel1.Controls.Add(this.button2, 1, 0);
			this.tableLayoutPanel1.Controls.Add(this.checkBox1, 2, 0);
			this.tableLayoutPanel1.Location = new System.Drawing.Point(278, 260);
			this.tableLayoutPanel1.Name = "tableLayoutPanel1";
			this.tableLayoutPanel1.RowCount = 1;
			this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
			this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 33F));
			this.tableLayoutPanel1.Size = new System.Drawing.Size(392, 33);
			this.tableLayoutPanel1.TabIndex = 4;
			// 
			// button1
			// 
			this.button1.Location = new System.Drawing.Point(3, 3);
			this.button1.Name = "button1";
			this.button1.Size = new System.Drawing.Size(124, 27);
			this.button1.TabIndex = 0;
			this.button1.Text = "Добавить пункт ТТ";
			this.button1.UseVisualStyleBackColor = true;
			this.button1.Click += new System.EventHandler(this.Button1Click);
			// 
			// button2
			// 
			this.button2.Enabled = false;
			this.button2.Location = new System.Drawing.Point(133, 3);
			this.button2.Name = "button2";
			this.button2.Size = new System.Drawing.Size(124, 27);
			this.button2.TabIndex = 1;
			this.button2.Text = "Изменить пункт ТТ";
			this.button2.UseVisualStyleBackColor = true;
			this.button2.Click += new System.EventHandler(this.Button2Click);
			// 
			// checkBox1
			// 
			this.checkBox1.Location = new System.Drawing.Point(263, 3);
			this.checkBox1.Name = "checkBox1";
			this.checkBox1.Size = new System.Drawing.Size(126, 27);
			this.checkBox1.TabIndex = 2;
			this.checkBox1.Text = "Спец. символы";
			this.checkBox1.UseVisualStyleBackColor = true;
			// 
			// button3
			// 
			this.button3.Location = new System.Drawing.Point(12, 9);
			this.button3.Name = "button3";
			this.button3.Size = new System.Drawing.Size(87, 10);
			this.button3.TabIndex = 5;
			this.button3.Text = "button3";
			this.button3.UseVisualStyleBackColor = true;
			this.button3.Click += new System.EventHandler(this.createTechReqs);
			// 
			// MainForm
			// 
			this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
			this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			this.ClientSize = new System.Drawing.Size(1236, 449);
			this.Controls.Add(this.button3);
			this.Controls.Add(this.tableLayoutPanel1);
			this.Controls.Add(this.rightListbox);
			this.Controls.Add(this.midTexbox);
			this.Controls.Add(this.midListbox);
			this.Controls.Add(this.leftListbox);
			this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
			this.MaximizeBox = false;
			this.Name = "MainForm";
			this.Text = "Модуль создания ТТ";
			this.tableLayoutPanel1.ResumeLayout(false);
			this.ResumeLayout(false);
			this.PerformLayout();

		}
	}
}
