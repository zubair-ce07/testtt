class User {
    constructor(number, username, id, avatar_url, github_url) {
        this.number = number;
        this.username = username;
        this.id = id;
        this.avatar_url = avatar_url;
        this.github_url = github_url;
    }
    
    /**
     * Creates a user card given the data stored at creation time of the object
     *
     * @author: mabdullahz
     * @this {User}
     * @returns {object} User card as an HTML element
     */
    getCard() {
        let userCard = document.createElement("div");
        userCard.className = CARD_CLASS_NAMES;
        userCard.style = CARD_STYLE;

        userCard.innerHTML = `<div class="card-header text-bold">${this.number}</div>
                                <img class="card-img-top" src="${this.avatar_url}" alt="Card image cap">

                                <div class="card-body">
                                    <h5 class="card-title text-center">${this.username}</h5>
                                </div>

                                <div class="card-footer bg-secondary text-center">
                                    <a href="profile.html?username=${this.username}" class="btn btn-success">View Profile</a>
                                </div>
                            </div>`;
        return userCard;
    }
}
