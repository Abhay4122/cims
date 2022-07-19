const cacheArr = ['/']
const CACHE_NAME = 'cache-v10'

// install the service worker
self.addEventListener('install', e => {
  console.log('Worker is installed')

  //   e.waitUntil(
  //     caches.open(CACHE_NAME).then(cache => {
  //       console.log('Opened cache')
  //       cache.addAll(cacheArr).then(() => self.skipWaiting())
  //     })
  //   )
})

// Use the service worker
self.addEventListener('activate', e => {
  console.log('Worker is activated')
  e.waitUntil(
    caches.keys().then(nams => {
      return Promise.all(
        nams.map(cnam => {
          if (CACHE_NAME !== cnam) {
            console.log('Worker is deleted')
            return caches.delete(cnam)
          }
        })
      )
    })
  )
})

// // Fetch the service worker
// self.addEventListener('fetch', e => {
//   e.respondWith(
//     caches.match(e.request).then(resp => {
//       if (resp) {
//         return resp
//       }
//       return fetch(e.request).catch(() => () => caches.match(e.request))
//     })
//   )
// })

// sync the response from server and worker
self.addEventListener('fetch', fetchE => {
  console.log('Hi')
  fetchE.respondWith(
    fetch(fetchE.request)
      .then(res => {
        console.log('Hello')
        const cacheRes = res.clone()

        caches.open(CACHE_NAME).then(cache => cache.put(fetchE.request, cacheRes))

        return res
      })
      .catch(() => caches.match(fetchE.request).then(res => res))
  )
})
