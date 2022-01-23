// Function for get or post data url
// Function for get data from API
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
    resp.msg ? Swal.fire({ icon: resp.alert_type, title: resp.title, text: resp.msg, html: resp.html }) : ''
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
