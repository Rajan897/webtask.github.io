class Chatbox {
  constructor() {
    this.args = {
      openButton: document.querySelector(".chatbox__button button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"),
      teamInfoContainer: document.querySelector(".team-info-container"),
    };

    this.state = false;
    this.messages = [];
    this.buttonContainer = this.args.chatBox.querySelector(".chatbox__button-container");
    this.textField = this.args.chatBox.querySelector(".chatbox__footer input");
    this.activeButton = null;
    this.buttonsDisplayed = false;
    this.hiMessageDisplayed = false;
  }

  display() {
    const { openButton, chatBox, sendButton } = this.args;

    openButton.addEventListener("click", () => this.toggleState(chatBox));

    sendButton.addEventListener("click", () => this.onSendButton(chatBox));

    this.textField.addEventListener("keyup", ({ key }) => {
      if (key === "Enter") {
        this.onSendButton(chatBox);
        const inputValue = this.textField.value.trim().toLowerCase();
        if (inputValue === "hi" && !this.buttonsDisplayed) {
          this.displayButtons();
        }
      }
    });
  }

  toggleState(chatbox) {
    this.state = !this.state;

    if (this.state) {
      chatbox.classList.add("chatbox--active");
    } else {
      chatbox.classList.remove("chatbox--active");
    }
  }

  onSendButton(chatbox) {
    let text = this.textField.value.trim();
    if (text === "") {
      return;
    }

    let msg = { name: "User", message: text };
    this.messages.push(msg);

    if (text.toLowerCase() === "hi" && !this.buttonsDisplayed) {
      const hiResponse = { name: "Sam", message: "Hi, how can I help you?" };
      this.messages.push(hiResponse);
      this.updateChatText(chatbox);
      this.hiMessageDisplayed = true;
    } else {
      this.hideButtons();
      this.sendMessageAndFetchResponse(text, chatbox);
    }
  }

  displayButtons() {
    this.buttonContainer.innerHTML = "";

    this.buttonContainer.style.display = "flex";

    const skillUpdateButton = `<button class="chatbox__button_plum" data-option="skill-update">Technology Stack</button>`;
    const orgStructureButton = `<button class="chatbox__button_plum" data-option="org-structure">Organizational Structure</button>`;

    this.buttonContainer.innerHTML = skillUpdateButton + orgStructureButton;

    const skillUpdateButtonElement = this.buttonContainer.querySelector('.chatbox__button_plum[data-option="skill-update"]');
    const orgStructureButtonElement = this.buttonContainer.querySelector('.chatbox__button_plum[data-option="org-structure"]');

    skillUpdateButtonElement.addEventListener("click", () => this.handleSkillUpdate(chatbox));
    orgStructureButtonElement.addEventListener("click", () => this.handleOrgStructure(chatbox));

    this.buttonsDisplayed = true;
  }

  hideButtons() {
    this.buttonContainer.innerHTML = "";
    this.buttonContainer.style.display = "none";
    this.activeButton = null;
  }

  sendMessageAndFetchResponse(text, chatbox) {
    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: JSON.stringify({ message: text }),
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        let msg = { name: "Sam", message: data.answer };
        this.messages.push(msg);
        this.updateChatText(chatbox);
        this.textField.value = "";
      })
      .catch((error) => {
        console.error("Error:", error);
        this.updateChatText(chatbox);
        this.textField.value = "";
      });
  }

  updateChatText(chatbox) {
    let html = "";
    this.messages.reverse().forEach((item) => {
      let className = item.name === "Sam" ? "visitor" : "operator";
      html += `<div class="messages__item messages__item--${className}">${item.message}</div>`;
    });

    const chatmessage = this.args.chatBox.querySelector(".chatbox__messages");
    chatmessage.innerHTML = html;
  }

  handleSkillUpdate(chatbox) {
    const message = "Please select a project: Asgard, Isard, SNCT";
    let msg = { name: "Sam", message };
    this.messages.push(msg);
    this.updateChatText(chatbox);

    // Display further buttons after selecting a project
    this.displayProjectButtons();
  }

  displayProjectButtons() {
    this.buttonContainer.innerHTML = "";

    const asgardButton = `<button class="chatbox__button_plum" data-project="asgard">Asgard</button>`;
    const isardButton = `<button class="chatbox__button_plum" data-project="isard">Isard</button>`;
    const snctButton = `<button class="chatbox__button_plum" data-project="snct">SNCT</button>`;

    this.buttonContainer.innerHTML = asgardButton + isardButton + snctButton;

    const asgardButtonElement = this.buttonContainer.querySelector('.chatbox__button_plum[data-project="asgard"]');
    const isardButtonElement = this.buttonContainer.querySelector('.chatbox__button_plum[data-project="isard"]');
    const snctButtonElement = this.buttonContainer.querySelector('.chatbox__button_plum[data-project="snct"]');

    asgardButtonElement.addEventListener("click", () => this.handleProjectDescription("asgard", chatbox));
    isardButtonElement.addEventListener("click", () => this.handleProjectDescription("isard", chatbox));
    snctButtonElement.addEventListener("click", () => this.handleProjectDescription("snct", chatbox));
  }

  handleProjectDescription(project, chatbox) {
    let message = "";
    if (project === "asgard") {
      message = "Join Asgard Team: Gateway to skywise project by upgrading your skills in Foundary: API, Template, AWS Pipeline, Mulesoft,ALGF,REP SAR Log Decompression,Merge Metadata to enter into Asgard Team.";
    } else if (project === "isard") {
      message = "Join ISARD Team: Gateway to Skywise project by upgrading your skills in Slate, Contour, Dashboard Designing , PySpark,Phonograph2";
    } else if (project === "snct") {
      message = "Join SNCT Team: Gateway to Skywise project by upgrading your skills in Pyspark, Contour, Data Lineage, Object Explorer, Object View, Ontology, Workshop. ";
    }

    let msg = { name: "Sam", message };
    this.messages.push(msg);
    this.updateChatText(chatbox);
  }

  handleOrgStructure(chatbox) {
    const message = "Please select a team: ASGARD, ISARD, SNCT";
    let msg = { name: "Sam", message };
    this.messages.push(msg);
    this.updateChatText(chatbox);

    // Display further buttons after selecting a team
    this.displayTeamButtons();
  }

  displayTeamButtons() {
    this.buttonContainer.innerHTML = "";

    const asgardButton = `<button class="chatbox__button_plum" data-team="asgard">ASGARD</button>`;
    const isardButton = `<button class="chatbox__button_plum" data-team="isard">ISARD</button>`;
    const snctButton = `<button class="chatbox__button_plum" data-team="snct">SNCT</button>`;

    this.buttonContainer.innerHTML = asgardButton + isardButton + snctButton;

    const asgardButtonElement = this.buttonContainer.querySelector('.chatbox__button_plum[data-team="asgard"]');
    const isardButtonElement = this.buttonContainer.querySelector('.chatbox__button_plum[data-team="isard"]');
    const snctButtonElement = this.buttonContainer.querySelector('.chatbox__button_plum[data-team="snct"]');

    asgardButtonElement.addEventListener("click", () => this.handleTeamDescription("asgard", chatbox));
    isardButtonElement.addEventListener("click", () => this.handleTeamDescription("isard", chatbox));
    snctButtonElement.addEventListener("click", () => this.handleTeamDescription("snct", chatbox));
  }

  handleTeamDescription(team, chatbox) {
    let message = "";
    if (team === "asgard") {
      message = "Asgard Team, led by Ankit, Prashanth, and Harsh, specializes in AWS, DynamoDB and Mulesoft.";
    } else if (team === "isard") {
      message = "ISARD, which stands for In-service Aircraft Referential Data, is managed by Kreethana and Pawan specialized in Foundry, Slate and Contour";
      
    } else if (team === "snct") {
      message = "SNCT (Supply Network Control Tower) provides visibility into baseline and tactical planning from Plants. This team is overseen by Aman and Kalim specialized in Foundry, Ontology";
    }

    let msg = { name: "Sam", message };
    this.messages.push(msg);
    this.updateChatText(chatbox);
  }
}

const chatbox = new Chatbox();
chatbox.display();
