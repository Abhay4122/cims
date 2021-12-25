// Function for create options for select
let select_option = data => {
  let options = ''

  for (let i of data) {
    options += `<option>${i}</option>`
  }

  return options
}

// Function for get or post data url
get_post = async (url, body) => {
  this.loa_der_show()
  let promise = new Promise((resolve, reject) => {
    fetch(url, { method: 'POST', body: body }).then(response =>
      response.ok ? resolve(response.json()) : reject(new Error('Got some error to get record.'))
    )
  }).catch(alert)
  let resp = await promise
  resp.message
    ? Swal.fire({ icon: resp.msg_typ, text: resp.message }).then(result =>
        result.isConfirmed ? (resp.redirect ? this.get_tariff($('#select_sites').val()) : '') : ''
      )
    : ''
  return resp
}

let sub_form = (data, form_id) => {
  //   let submitable_data = {}
  //   for (let i in data) {
  //     console.log($(`#${i.split('*')[1]}`).val())
  //   }
  console.log('Hello')
  $('#' + form_id).submit(function (e) {
    e.preventDefault()
  })
}

// Function define for create the form
let create_form = (data, id, csrf) => {
  let form_html = `
    <form id='${id}'>
    ${csrf}
  `

  for (let i in data) {
    let input_type = i.split('*')

    if (input_type[0] == 'select') {
      form_html += `
            <div class='col-md-6'>
                <label>${data[i][0]}</label>
                <select id='${input_type[1]}' class='form-control' style='margin: 10px auto' required>
                    <option>Select ${data[i][0]}</option>
                    ${select_option(data[i][1])}
                </select>
            </div>
        `
    } else if (input_type[0] == 'text') {
      form_html += `
            <div class='col-md-6'>
                <label>${data[i]}</label>
                <input type='text' id='${input_type[1]}' class='form-control' required />
            </div>
        `
    } else if (input_type[0] == 'tel') {
      form_html += `
            <div class='col-md-6'>
                <label>${data[i]}</label>
                <input type='tel' id='${input_type[1]}' class='form-control' required />
            </div>
        `
    } else if (input_type[0] == 'date') {
      form_html += `
            <div class='col-md-6'>
                <label>${data[i]}</label>
                <input type='date' id='${input_type[1]}' class='form-control' required />
            </div>
        `
    } else if (input_type[0] == 'file') {
      form_html += `
            <div class='col-md-6'>
                <label>${data[i]}</label>
                <input type='file' id='${input_type[1]}' class='form-control' accept='image/png, image/jpeg' />
            </div>
        `
    }
  }

  form_html += `
            <div class='col-md-6'>
                <br />
                <button class='btn btn-danger' onclick='sub_form(${data}, "${id}"})'>Submit</button>
            </div>
        </form>
    `

  return form_html
}
