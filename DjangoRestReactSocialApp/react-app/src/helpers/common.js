import Swal from 'sweetalert2'
import lodash from 'lodash'

const API_URL = process.env.REACT_APP_API_URL

const Toast = Swal.mixin({
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 3000,
  timerProgressBar: true,
  onOpen: (toast) => {
    toast.addEventListener('mouseenter', Swal.stopTimer)
    toast.addEventListener('mouseleave', Swal.resumeTimer)
  }
})

export function toast (icon, title) {
  Toast.fire({
    icon,
    title
  })
}

export function msgAlert (state, msg) {
  if (state === 'success') {
    Swal.fire('Success!', msg, 'success')
  } else if (state === 'failure') {
    Swal.fire('Failed!', msg, 'error')
  }
}

export function deepCopy (data) {
  return JSON.parse(JSON.stringify(data))
}

export function _exists (obj, keyPath) {
  return lodash.get(obj, keyPath)
}

export function toFormData (obj) {
  const formData = new FormData()
  Object.keys(obj).forEach((key) => {
    formData.append(key, obj[key])
  })
  return formData
}

export function resolveImageUrl (url) {
  if (url.includes('http')) {
    return url
  } else {
    if (url[0] === '/') { return `${API_URL}${url}` } else { return `${API_URL}/media/${url}` }
  }
}

export function confirmBox (callback) {
  Swal.fire({
    title: 'Are you sure?',
    text: "You won't be able to revert this!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, delete it!'
  }).then((result) => {
    callback(result)
    // if (result.value) {
    //   Swal.fire(
    //     'Deleted!',
    //     'Your file has been deleted.',
    //     'success'
    //   )
    // }
  })
}
