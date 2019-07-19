class Repo {
    constructor(repoName, repoDescription, repoCreated, repoUpdated, repoWatchers, repoLanguage, repoForks, repoIssuesCount, repoLicense, repoURL) {
        this.repoName = repoName;
        this.repoDescription = repoDescription;
        this.repoCreated = repoCreated;
        this.repoUpdated = repoUpdated;
        this.repoWatchers = repoWatchers;
        this.repoLanguage = repoLanguage;
        this.repoForks = repoForks;
        this.repoIssuesCount = repoIssuesCount;
        this.repoLicense = repoLicense; 
        this.repoURL = repoURL;
    }

    /**
     * Creates a repo card given the data stored at creation time of the object
     *
     * @author: mabdullahz
     * @this {Repo}
     * @returns {object} REpo card as an HTML element
     */
    getCard() {
        let repoCard = document.createElement("div");
        repoCard.className = CARD_CLASS_NAMES
        repoCard.style = CARD_STYLE;
        
        repoCard.innerHTML =    `<div class="card-header text-center">
                                <div class="row">
                                    <div class="col-sm">
                                        <p class="text-center font-weight-bold"> ${this.repoName} </p> 
                                    </div>

                                    <div class="col-sm text-right my-auto">
                                        <a href="${this.repoURL}" target="__blank" class="btn btn-primary">View on Github</a>
                                    </div>
                                </div>
                                <p> Language: ${this.repoLanguage} </p> 
                                <p> License: ${this.repoLicense} </p>
                            </div>

                            <div class="card-body">
                                <p> ${this.repoDescription} </p>
                            </div>

                            <div class="card-footer bg-secondary text-center">
                                <p class="bg-danger p-1 medium"> Created at: ${this.repoCreated} </p>
                                <p class="bg-info p-1"> Last Updated: <br> ${this.repoUpdated} </p>
                            </div>
                            
                            <div class="card-footer bg-secondary medium">
                                <div class="row text-center">
                                    <div class="col-sm bg-primary">
                                        Watchers: ${this.repoWatchers}
                                    </div>
                                    <div class="col-sm bg-warning">
                                        Forks: ${this.repoForks}
                                    </div>
                                    <div class="col-sm bg-danger">
                                        Issues: ${this.repoIssuesCount}
                                    </div>
                                </div>
                            </div>`;
        return repoCard;
    }
}
