class form_handler {
  constructor(url, id) {
    this.loa_der_show = () => $('#loa_der').css('display', 'grid')
    this.loa_der_hide = () => $('#loa_der').css('display', 'none')
    this.loader = () => `<i class="fa fa-spinner fa-spin" style="font-size:24px"></i>`
    this.url = url
    this.id = id
  }

  // Function for get or post data url
  get_post = async (url = '', body = false, head = false) => {
    let promise = new Promise((resolve, reject) => {
      if (head) {
        fetch(url ? url : this.url, { method: 'post', headers: { Accept: 'application/json' }, body: body }).then(response =>
          response.ok ? resolve(response.json()) : reject(new Error('Got some error to get record.'))
        )
      } else {
        fetch(url ? url : this.url).then(response => (response.ok ? resolve(response.json()) : reject(new Error('Got some error to get record.'))))
      }
    }).catch(alert)

    let resp = await promise
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
    } catch (err) {}
    console.log(resp)
    return resp
  }

  // Function for create options for select
  select_option = data => {
    let options = ''

    for (let i in data) {
      options += `<option value='${data[i]}'>${i}</option>`
    }

    return options
  }

  // Function define for create the form
  create_form = (data, csrf) => {
    let form_html = `
    <form id='${this.id}_form'>
      ${csrf}
  `

    for (let i in data) {
      let input_type = i.split('#')

      if (input_type[0] == 'select') {
        form_html += `
        <div class='col-md-${data['row']}'>
          <label>${data[i][0]}</label>
          <select id='${input_type[1]}_id' name='${input_type[1]}' class='form-control' style='margin: 10px auto' required>
            <option>Select ${data[i][0]}</option>
            ${this.select_option(data[i][1])}
          </select>
        </div>
      `
      } else if (input_type[0] == 'textarea') {
        form_html += `
        <div class='col-md-${data['row']}'>
          <label>${data[i][0]}</label>
          <textarea id='${input_type[1]}_id' name='${input_type[1]}' class='form-control' ${data[i][1]['attr']} ${
          data[i][0].includes('*') ? 'required' : ''
        }> </textarea>
        </div>
      `
      } else if (input_type[0] != 'row') {
        form_html += `
        <div class='col-md-${data['row']}'>
          <label>${data[i][0]}</label>
          <input type='${input_type[0]}' id='${input_type[1]}_id' name='${input_type[1]}' class='form-control' ${
          data[i][1] ? data[i][1]['attr'] : ''
        } ${data[i][0].includes('*') ? 'required' : ''} />
        </div>
      `
      }
    }

    form_html += `
      <div class='col-md-12'>
        <br />
        <button class='btn btn-danger'>Submit</button>
      </div>
    </form>
  `

    return form_html
  }

  crud = async (url, btn) => {
    if (btn == 'Edit') {
      let data = await this.get_post(url)
      console.log(data)
      await this.add_edit_modal('Update student', data)
      console.log('Hello')
    } else if (btn == 'View') {j
      // let data = this.get_post(url)
      // console.log(data)
    } else if (btn == 'Delete') {
      // let data = this.get_post(url)
      // console.log(data)
    }
  }

  // Function define to create the dynamic data table
  create_tbl = async (url, id, conf = {}, action = {}) => {
    try {
      let data = await this.get_post(url)
      let th = []

      for (let i in data[0]) {
        let heading = i.replaceAll('_', ' ')
        th.push(heading.charAt(0).toUpperCase() + heading.slice(1))
      }

      // For Single column action
      if (action) {
        th.push('Action')

        let action_html = ''

        for (let i in action) {
          action_html += `
            <i class="fa fa-${
              i == 'Edit' ? 'pencil' : i == 'View' ? 'eye' : i == 'Delete' ? 'trash' : ''
            } hover" style="margin-left: 7px; margin-right: 7px;" id="${i}"></i>
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

      for (let i of th) {
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

      for (let j of data) {
        let col = []
        for (let k in j) {
          col.push(j[k])
        }
        _tbl.row.add(col).draw(false)
      }

      $(`#${tbl_id} tbody`).on('click', 'i', e => {
        let cam_row = _tbl.row($(e.target).parents('tr')).data()
        let btn_id = e.target.id
        this.crud(`${action[btn_id][1]}?id=${cam_row[0]}`, btn_id)
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
    let dt_tbl = $('#' + id).DataTable({
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
      iDisplayLength: 15,
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
  init_modal = async (id, header, body, value) => {
    $(`#${id} #modal_header`).text(header)
    $(`#${id} #modal_body`).html(body)
    $(`#${id}`).modal()

    let form_data = new FormData(document.getElementById(`${this.id}_form`))
    let url = this.url

    if (value) {
      for (let i in value) {
        if (i == 'id') {
          url = `${this.url}?id=${value[i]}`
        } else {
          form_data.set(i, value[i])
        }
      }
    }

    $(`#${this.id}_form`).on('submit', async e => {
      e.preventDefault()
      await this.get_post(url, form_data, true)
    })
  }
}

// Function for get or post data url
let get_post = async (url, body = false, head = false) => {
  let promise = new Promise((resolve, reject) => {
    if (head) {
      fetch(url, { method: 'post', headers: { Accept: 'application/json' }, body: body }).then(response =>
        response.ok ? resolve(response.json()) : reject(new Error('Got some error to get record.'))
      )
    } else {
      fetch(url).then(response => (response.ok ? resolve(response.json()) : reject(new Error('Got some error to get record.'))))
    }
  }).catch(alert)

  let resp = await promise
  try {
    resp.msg
      ? Swal.fire({ icon: resp.alert_type, title: resp.title, text: resp.msg, html: resp.html }).then(result => {
          result.isConfirmed && resp.lod_link ? (window.location.href = resp.lod_link) : ''
        })
      : ''
  } catch (err) {}
  console.log(resp)
  return resp
}

let sub_form = async (url, id) => {
  let form_data = new FormData(document.getElementById(id))

  //  ***************** OR ************************
  // form_data.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());

  // for (let i in data){
  //   let input_type = i.split('*');

  //   if(input_type[0] != 'file'){
  //     form_data.append(input_type[1], $('#' + input_type[1] + '_id').val());
  //   } else {
  //     form_data.append(input_type[1], document.getElementById(input_type[1] + '_id').files[0]);
  //   }
  // }

  // Learning curve
  // console.log(form_data.get('photo'));
  // console.log(form_data.has('dob'));
  // console.log(form_data.delete('dob'));

  // ************* Notice *************
  // https://javascript.info/formdata

  await get_post(url, form_data, true)

  // let xhr = new XMLHttpRequest();

  //   // Add any event handlers here...
  //   xhr.open('POST', 'std-registration', true);
  //   xhr.send(form_data);

  //   function success() {
  //     var data = JSON.parse(this.responseText);
  //     console.log(data);
  // }

  // function error(err) {
  //     console.log('Error Occurred :', err);
  // }

  // var xhr = new XMLHttpRequest();
  // xhr.onload = success;
  // xhr.onerror = error;
  // xhr.open('GET', 'https://api.github.com/users/swapnilbangare');
  // xhr.send();

  // // ****************** VS ********************
  // fetch('https://api.github.com/users/swapnilbangare')
  //     .then(function (response) {
  //         console.log(response);
  //     })
  //     .catch(function (err) {
  //         console.log("Something went wrong!", err);
  //     });
}

// Function define for perform CRUD operation
let crud = data => {
  console.log(data)
}

// Function for create options for select
let select_option = data => {
  let options = ''

  for (let i in data) {
    options += `<option value='${data[i]}'>${i}</option>`
  }

  return options
}

// Function define for create the form
let create_form = (data, id, csrf) => {
  let form_html = `
    <form id='${id}'>
      ${csrf}
  `

  for (let i in data) {
    let input_type = i.split('#')

    if (input_type[0] == 'select') {
      form_html += `
        <div class='col-md-${data['row']}'>
          <label>${data[i][0]}</label>
          <select id='${input_type[1]}_id' name='${input_type[1]}' class='form-control' style='margin: 10px auto' required>
            <option>Select ${data[i][0]}</option>
            ${select_option(data[i][1])}
          </select>
        </div>
      `
    } else if (input_type[0] == 'textarea') {
      form_html += `
        <div class='col-md-${data['row']}'>
          <label>${data[i][0]}</label>
          <textarea id='${input_type[1]}_id' name='${input_type[1]}' class='form-control' ${data[i][1]['attr']} ${
        data[i][0].includes('*') ? 'required' : ''
      }> </textarea>
        </div>
      `
    } else if (input_type[0] != 'row') {
      form_html += `
        <div class='col-md-${data['row']}'>
          <label>${data[i][0]}</label>
          <input type='${input_type[0]}' id='${input_type[1]}_id' name='${input_type[1]}' class='form-control' ${
        data[i][1] ? data[i][1]['attr'] : ''
      } ${data[i][0].includes('*') ? 'required' : ''} />
        </div>
      `
    }
  }

  form_html += `
      <div class='col-md-12'>
        <br />
        <button class='btn btn-danger'>Submit</button>
      </div>
    </form>
  `

  return form_html
}

// Function define to create the dynamic data table
let create_tbl = async (th, data, id, conf = {}, action = {}) => {
  try {
    // For multicolumn Action
    /* for (let i in action) {
      th.push(i)
      conf.columnDefs.push({
        targets: action[i][0],
        data: null,
        defaultContent: `
          <i class="fa fa-${i == 'Edit' ? 'pencil' : i == 'View' ? 'eye' : i == 'Delete' ? 'trash-o' : ''} hover" onclick='crud(${action[i][1]})'></i>
        `
      })
    } */

    // For Single column action
    if (action) {
      th.push('Action')

      let action_html = ''

      for (let i in action) {
        action_html += `
          <i class="fa fa-${
            i == 'Edit' ? 'pencil' : i == 'View' ? 'eye' : i == 'Delete' ? 'trash' : ''
          } hover" style="margin-left: 7px; margin-right: 7px;" onclick='crud(${action[i][1]})'></i>
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

    for (let i of th) {
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

    _tbl = await this.def_dt_tbl(tbl_id, conf, action)

    for (let j of data) {
      let col = []
      for (let k in j) {
        col.push(j[k])
      }
      _tbl.row.add(col).draw(false)
    }
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
def_dt_tbl = async (id, conf, action) => {
  let dt_tbl = $('#' + id).DataTable({
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
    iDisplayLength: 15,
    ...conf
  })

  $('#' + id + '_filter label').addClass('m-1')
  $('#' + id + '_filter input').addClass('form-control')
  $('#' + id + '_filter input').attr('placeholder', 'Search data ...')
  $('#' + id + '_length select').addClass('form-control')
  $('#' + id + '_length select').addClass('py-0')
  return dt_tbl
}
