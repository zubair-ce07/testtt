class Repository {
    constructor(name, description, created, updated, watchers, language, forks, issues, license, url) {
        this.name = name;
        this.description = description;
        this.created = created;
        this.updated = updated;
        this.watchers = watchers;
        this.language = language;
        this.forks = forks;
        this.issues = issues;
        this.license = license; 
        this.url = url;
    }

    /**
     * Creates a HTML card for Repository Object given the data stored at creation time of the object
     *
     * @author: mabdullahz
     * @this {Repository}
     * @returns {object} Repository card as an HTML element
     */
    generateRepoCard() {
        let repoCard = document.createElement("div");

        repoCard.className = CARD_CLASS_NAMES
        repoCard.style = CARD_STYLE;
        repoCard.innerHTML = this.generateRepoCardInnerHtml();

        return repoCard;
    }

    generateRepoCardInnerHtml() {
        return `<div class="card-header text-center">
                    <div class="row">
                        <div class="col-sm">
                            <p class="text-center font-weight-bold"> ${this.name} </p> 
                        </div>

                        <div class="col-sm text-right my-auto">
                            <a href="${this.url}" target="__blank" class="btn btn-primary">View on Github</a>
                        </div>
                    </div>
                    <p> Language: ${this.language} </p> 
                    <p> License: ${this.license} </p>
                </div>

                <div class="card-body">
                    <p> ${this.description} </p>
                </div>

                <div class="card-footer bg-secondary text-center">
                    <p class="bg-danger p-1 medium"> Created at: ${this.created} </p>
                    <p class="bg-info p-1"> Last Updated: <br> ${this.updated} </p>
                </div>
                
                <div class="card-footer bg-secondary medium">
                    <div class="row text-center">
                        <div class="col-sm bg-primary">
                            Watchers: ${this.watchers}
                        </div>
                        <div class="col-sm bg-warning">
                            Forks: ${this.forks}
                        </div>
                        <div class="col-sm bg-danger">
                            Issues: ${this.issues}
                        </div>
                    </div>
                </div>`;
    }
}
