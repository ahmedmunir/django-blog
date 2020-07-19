// Add new comment using Ajax request

document.querySelector('.add_comment').addEventListener('click', e => {

    // We must prevent default behaviour of <a> or <button>
    // to not redirect to another route
    e.preventDefault();


    let data = new FormData()
    comment = document.querySelector('.comment_text').value;
    data.append('text', comment);

    // we work at Django so we can use url at any static file
    // let url = '{% url "comment-create" object.id %}'
    let url = `${window.location.href}comment/new/`
    fetch(url, {
        method: "POST",
        body: data,

        // Very important for security and use csrf_token
        // Any Post request must have csrf_token for protection.
        headers: {
            // 'X-CSRFToken': '{{ csrf_token }}'
            'X-CSRFToken': document.querySelector('input[type=hidden]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        
        // If comment added to DB successfully
        if (data['result'] == 'Success') {
            let new_comment = data['new_comment'];
            let container = document.querySelector('.comments_container');
            
            // Add new comment 
            container.insertAdjacentHTML('beforeend',
            `
                <div class="comment">
                    <div class="comment-header d-flex justify-content-between">
                        <div class="user d-flex align-items-center">
                            <div class="image">
                                <img src="${data['url']}" alt="..." class="img-fluid rounded-circle">
                            </div>
                            <div class="title">
                                <strong href="${data['user_posts']}">${data['username']}</strong>
                                <span class="date">${data['date']}</span>
                            </div>
                        </div>
                    </div>
                    <div class="comment-body">
                        <p>${data['text']}</p>
                        <a class='btn btn-secondary btn-sm mt-1 mb-1' href="${data['comment_update']}">Update</a>
                        <a class='btn btn-danger btn-sm mt-1 mb-1' href="${data['comment_delete']}">Delete</a>
                    </div>
                </div>
            `
            )
        }

        //clear text field after add comment
        document.querySelector('#id_text').value = "";
    })
})

