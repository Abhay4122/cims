class form_handler {
  constructor() {
    this.loa_der_show = () => $('#loa_der').css('display', 'grid')
    this.loa_der_hide = () => $('#loa_der').css('display', 'none')
    this.loader = () => `<i class="fa fa-spinner fa-spin" style="font-size:24px"></i>`
    this.value = false // Update data as value
    this.csrf = this.getCookie('csrftoken')
  }

  // Function define to get cooki
  getCookie = cname => {
    let name = cname + '='
    let decodedCookie = decodeURIComponent(document.cookie)
    let ca = decodedCookie.split(';')
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i]
      while (c.charAt(0) == ' ') {
        c = c.substring(1)
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length)
      }
    }
    return ''
  }

  // Function for get or post data url
  get_post = async (url = '', body = false, method = false) => {
    const promise = new Promise((resolve, reject) => {
      if (method == 'post' || method == 'POST' || method == 'put' || method == 'PUT') {
        fetch(url ? url : this.url, { method: method, headers: { Accept: 'application/json', 'X-CSRFToken': this.csrf }, body: body }).then(
          response => (response.ok ? resolve(response.json()) : reject(new Error('Got some error to get record.')))
        )
      } else if (method == 'delete' || method == 'DELETE') {
        fetch(url ? url : this.url, { method: method, headers: { 'X-CSRFToken': this.csrf } }).then(response =>
          response.ok ? resolve(response.json()) : reject(new Error('Got some error to get record.'))
        )
      } else {
        fetch(url ? url : this.url).then(response => (response.ok ? resolve(response.json()) : reject(new Error('Got some error to get record.'))))
      }
    }).catch(alert)

    const resp = await promise
    try {
      resp.msg
        ? Swal.fire({
            icon: resp.alert_type,
            title: resp.title,
            text: resp.msg,
            html: resp.html,
            allowOutsideClick: false,
            allowEscapeKey: false
          }).then(result => {
            result.isConfirmed && resp.lod_link ? (window.location.href = resp.lod_link) : ''
          })
        : ''
    } catch (err) {
      console.log(err)
    }
    return resp
  }

  // Function for create options for select
  select_option = (data, id) => {
    let options = ''

    for (const i in data) {
      options += `<option value='${data[i]}' ${this.value ? (data[i] == this.value[id] ? 'selected' : '') : ''}>${i}</option>`
    }

    return options
  }

  field_generator = async data => {
    let form_html = ''

    for (const i in data) {
      const input_type = i.split('#')
      let label = data[i][0]
      try {
        if (data[i][0].includes('#')) {
          label = data[i][0].split('#')[0]
        }
      } catch (err) {}

      if (input_type[0] == 'select') {
        form_html += `
        <div class='col-md-${data['row']}'>
          <label style='font-size: 10px; margin-bottom: 0; font-weight: 400;'>${label}</label>
          <select name='${input_type[1]}' id='${input_type[1]}_id' class='form-control' style='margin: 10px auto' required>
            <option>Select ${label}</option>
            ${this.select_option(data[i][1], input_type[1])}
          </select>
        </div>
      `
      } else if (input_type[0] == 'textarea') {
        form_html += `
        <div class='col-md-${data['row']}'>
          <label style='font-size: 10px; margin-bottom: 0; font-weight: 400;'>${label}</label>
          <textarea name='${input_type[1]}' id='${input_type[1]}_id' class='form-control' ${data[i][1]['attr']} ${
          data[i][0].includes('*') ? 'required' : data[i][0].includes('#') ? 'disabled' : ''
        }> ${this.value ? this.value[input_type[1]] : ''} </textarea>
        </div>
      `
      } else if (input_type[0] == 'hidden') {
        form_html += `<input type='${input_type[0]}' name='${input_type[1]}' id='${input_type[1]}_id' />`
      } else if (input_type[0] != 'row') {
        form_html += `
        <div class='col-md-${data['row']}'>
          <label style='font-size: 10px; margin-bottom: 0; font-weight: 400;'>${label}</label>
          <input type='${input_type[0]}' name='${input_type[1]}' id='${input_type[1]}_id' value='${
          this.value ? this.value[input_type[1]] : ''
        }' class='form-control' ${data[i][1] ? data[i][1]['attr'] : ''} ${
          data[i][0].includes('*') ? 'required' : data[i][0].includes('#') ? 'disabled' : ''
        } />
        </div>
      `
      }
    }

    return form_html
  }

  // Function define for create the form
  create_form = async data => {
    let form_html = `
    <form id='${this.id}_form'>
  `
    form_html += await this.field_generator(data)

    form_html += `
      <div id='extra_fields'></div>
      <div class='col-md-12'>
        <br />
        <button class='btn btn-danger' name='Submit ${this.id} form'>Submit</button>
      </div>
    </form>
  `
    return form_html
  }

  // Function define to create the dynamic data table
  create_tbl = async (url, id, conf = {}, action = {}) => {
    try {
      let data = await this.get_post(url)
      let th = []

      for (const i in data[0]) {
        const heading = i.replaceAll('_', ' ')
        th.push(heading.charAt(0).toUpperCase() + heading.slice(1))
      }

      // For Single column action
      if (action) {
        th.push('Action')

        let action_html = ''

        for (const i in action) {
          action_html += `
            <span class="fa fa-${
              i == 'Edit' ? 'pencil' : i == 'View' ? 'eye' : i == 'Delete' ? 'trash' : ''
            } hover" style="margin-left: 7px; margin-right: 7px;" id="${i}"></span>
          `
        }
        conf.columnDefs.push({
          targets: -1,
          data: null,
          defaultContent: action_html
        })
      }

      let tbl_id = id + '_tbl'
      let _tbl = ''
      let tbl = `
        <table id='${tbl_id}' class='tab_le'>
          <thead class='t_head'>
            <tr>
      `

      for (const i of th) {
        tbl += `<th>${i}</th>`
      }

      tbl += `
            </tr>
          </thead>
        </table>
      `

      $('#' + id).html(tbl)

      if (jQuery.isEmptyObject(data)) {
        $('#' + id).html(`
          <div class='row py-5'>
            <div class='col-12 text-center'>
              <h2>Sorry !!</h2>
              <h4>No data found.</h4>
            </div>
          </div>
        `)
        return
      }

      _tbl = await this.def_dt_tbl(tbl_id, conf)

      for (const j of data) {
        let col = []
        for (let k in j) {
          col.push(j[k])
        }
        _tbl.row.add(col).draw(false)
      }

      $(`#${tbl_id} tbody`).on('click', 'span', e => {
        const row = _tbl.row($(e.target).parents('tr')).data()
        const btn_id = e.target.id
        try {
          this.crud(`${action[btn_id][1]}?id=${row[0]}`, btn_id)
        } catch (err) {
          this.row_click(btn_id, row)
        }
      })
    } catch (e) {
      $('#' + id).html(`
        <div class='row py-5'>
          <div class='col-12 text-center'>
            <h2>Sorry !!</h2>
            <h4>No data found.</h4>
          </div>
        </div>
      `)
    }
  }

  // Data table define
  def_dt_tbl = async (id, conf) => {
    const dt_tbl = $('#' + id).DataTable({
      language: {
        search: '',
        lengthMenu: '_MENU_'
      },
      dom:
        "<'row'" +
        // Button
        //"<'col-sm-12 col-md-5'B>" +
        // Search
        "<'col-12'f>" +
        '>' +
        // Table
        "<'row dt-table'<'col-sm-12 col-md-12'tr>>" +
        // Pagination
        "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
      //dom: 'Bfrtip',
      //buttons: [{
      //    extend: 'csvHtml5',
      //    text: 'Consumer EB DG consumption CSV',
      //    title: 'Property_maintenance',
      //    exportOptions: {
      //        columns: [1,2, 3, 4, 5]
      //    }
      //}],
      iDisplayLength: 50,
      ...conf
    })

    $('#' + id + '_filter label').addClass('m-1')
    $('#' + id + '_filter input').addClass('form-control')
    $('#' + id + '_filter input').attr('placeholder', 'Search data ...')
    $('#' + id + '_length select').addClass('form-control')
    $('#' + id + '_length select').addClass('py-0')
    return dt_tbl
  }

  // Function defin to init content in modal
  init_modal = async (header, body, is_method = false) => {
    $(`#${this.modal_id} #modal_header`).text(header)
    $(`#${this.modal_id} #modal_body`).html(body)

    $(`#${this.modal_id}`).modal()

    $(`#${this.id}_form`).on('submit', async e => {
      e.preventDefault()

      const form_data = new FormData(document.getElementById(`${this.id}_form`))
      const method = is_method ? is_method : this.value ? 'put' : 'post'

      let url = this.url.split('?')[0]
      url = this.value ? `${url}?id=${this.value['id']}` : url

      await this.get_post(url, form_data, method)
    })
  }

  // CRUD operation for the table
  crud = async (url, btn) => {
    if (btn == 'Edit') {
      this.value = await this.get_post(url)
      await this.add_edit_modal(`Update ${this.id} detail`)
    } else if (btn == 'View') {
      const data = await this.get_post(url)
      await this.view_data_modal(`View ${this.id} detail`, data)
    } else if (btn == 'Delete') {
      Swal.fire({
        icon: 'warning',
        title: 'Are you sure ?',
        text: 'to delete the record !!',
        showCancelButton: true,
        allowOutsideClick: false,
        allowEscapeKey: false
      }).then(result => {
        result.isConfirmed ? this.get_post(url, false, 'delete') : ''
      })
    }
  }

  // Function defin to show the data
  view_data_modal = async (header, data) => {
    let html = '<div class="row">'

    html +=
      data['photo'] !== undefined
        ? data['photo']
          ? `<div class="col-sm-6 text-right" style="margin-bottom: 10px;">Photo : </div> <div class="col-sm-6" style="margin-bottom: 10px;"><img src="${data['photo']}" height="100px" alt="Show image" /></div>`
          : `<div class="col-sm-6 text-right" style="margin-bottom: 10px;">Photo : </div> <div class="col-sm-6" style="margin-bottom: 10px;">N/A</div>`
        : ''

    for (const i in data) {
      html +=
        i == 'photo'
          ? ''
          : `<div class="row"><div class="col-sm-6 text-right" style="margin-bottom: 10px;">${
              i.charAt(0).toUpperCase() + i.slice(1)
            } : </div> <div class="col-sm-6" style="margin-bottom: 10px;">${data[i]}</div></div>`
    }

    html += '</div>'

    $(`#${this.modal_id} #modal_header`).text(header)
    $(`#${this.modal_id} #modal_body`).html(html)
    $(`#${this.modal_id}`).modal()
  }
}
