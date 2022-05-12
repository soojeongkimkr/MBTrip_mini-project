// 리뷰와 날짜 저장
function infj_write_review() {
    let write = $('#write').val()
    let date = new Date().toISOString()
    console.log(write, date)

    $.ajax({
        type: "POST",
        url: "/write/infj",
        data: {write_give: write, date_give: date},
        success: function (response) {
            alert(response["msg"])
            window.location.reload()
        }
    });
}

// 리뷰 쓴 시간이 얼마나 되었는지 보여주는 함수
// Date 오브젝트 간의 빼기 : 밀리초
function time2str(date) {
    let today = new Date()
    let time = (today - date) / 1000 / 60  // 분

    if (time < 60) {
        return parseInt(time) + "분 전"
    }
    time = time / 60  // 시간
    if (time < 24) {
        return parseInt(time) + "시간 전"
    }
    time = time / 24
    if (time < 7) {
        return parseInt(time) + "일 전"
    }
    return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}

// 리뷰 보여주기
function infj_show_review() {
    $('#list-box').empty();
    $.ajax({
        type: "GET",
        url: "/review/infj",
        data: {},
        success: function (response) {
            if (response['result'] == "success") {
                let reviews = response["reviews"]
                for (let i = 0; i < reviews.length; i++) {
                    let id = reviews[i]
                    let name = reviews[i]['username']
                    let date = new Date(reviews[i]['date'])
                    let time_before = time2str(date)
                    let review = reviews[i]['write']
                    let like = reviews[i]['like']
                    console.log(id, name, date, review,)
                    let temp_html = `<div class="box" id={$id['_id']}>
                                            <article class="media">
                                                <div class="media-left">
                                                    <figure class="image is-64x64">
                                                        <img src="https://cdn-icons-png.flaticon.com/512/569/569501.png" alt="Image">
                                                    </figure>
                                                </div>
                                                <div class="media-content">
                                                    <div class="content">
                                                        <p>
                                                            <strong>${name}</strong> <small>${time_before}</small>
                                                            <br>
                                                                ${review}
                                                        </p>
                                                    </div>
                                                    <nav class="level is-mobile">
                                                            <div class="feeling_div">
                                                                    <button class="button is-white" onclick="infj_like_review('${review}')" ><i class="fa-solid fa-heart"> ${like}</i> </button>
                                                                    <button class="button is-white" onclick="infj_delete_review('${id['_id']}')"><i class="fa-solid fa-trash-can"></i></button>
                                                            </div>
                                                        </nav>
                                                </div>
                                            </article>
                                        </div>`
                    $('#list-box').append(temp_html)
                }
            }
        }
    })
}

// 리뷰 삭제하기
function infj_delete_review(id) {
    $.ajax({
        type: 'POST',
        url: '/delete/infj',
        data: {
            id_give: id
        },
        success: function (response) {
            alert(response['msg']);
            window.location.reload();
        }
    });
}

// 좋아요 수
function infj_like_review(review) {
    $.ajax({
        type: 'POST',
        url: '/like/infj',
        data: {
            review_give: review
        },
        success: function (response) {
            alert(response['msg']);
            window.location.reload();
        }
    });
}