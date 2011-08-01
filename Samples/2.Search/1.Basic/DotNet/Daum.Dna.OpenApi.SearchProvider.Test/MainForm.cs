using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using Daum.Dna.OpenApi.SearchProvider.Responses;

namespace Daum.Dna.OpenApi.SearchProvider.Test
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            InitializeComponent();
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            Init();
        }

        private void Init()
        {
            rbAccu.Checked = true;
            cmbPage.SelectedIndex = 5;
            cmbResult.SelectedIndex = 5;
        }

        private void btnSearch_Click(object sender, EventArgs e)
        {
            string query = txtQuery.Text;
            int result = int.Parse(cmbResult.SelectedItem.ToString());
            int page = int.Parse(cmbPage.SelectedItem.ToString());
            string sort = "";
            if (rbAccu.Checked) sort = "accu";
            else sort = "date";

            try
            {
                //API호출
                BlogData data = OpenApiProvider.RequestBlogApi("{발급 받은 키를 입력하세요.}", query, result, page, sort, "rss", "");

                //Title만 리스트에 표시
                listResponse.DataSource = data.Items.Select(a=>a.Title).ToList();
            }
            catch(Exception ex)
            {
                MessageBox.Show(ex.Message,"오류 반환");
            }
        }
    }
}
