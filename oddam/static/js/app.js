document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.$slidesPagination = $el.querySelectorAll('.help--slides-pagination');
      // this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;


      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      // const page = e.target.dataset.id;
      const page = e.target.dataset.id;
      console.log(page);

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      page.classList.add("active");

      // Current slide
      this.currentSlide = page.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });

    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.$checkboxInputs = form.querySelectorAll('input[type=checkbox]');
      this.$catDivs = form.querySelectorAll('div.category');
      this.currentStep = 1;
      this.$fifthStepDiv = form.querySelector('div[data-step="5"]');
      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      this.$addressInput = form.querySelector('input[name="address"]');
      this.$cityInput = form.querySelector('input[name="city"]');
      this.$postcodeInput = form.querySelector('input[name="postcode"]');
      this.$phoneInput = form.querySelector('input[name="phone"]');
      this.$dateInput = form.querySelector('input[name="date"]');
      this.$timeInput = form.querySelector('input[name="time"]');
      this.$commentTextarea = form.querySelector('textarea[name="more_info"]');
      this.$bagsInput = form.querySelector('input[name="bags"]');
      this.$userId = form.querySelector('input[name="user_id"]');
      this.$divsTitle = form.querySelectorAll('div[data-step="3"] div.title');
      this.$thirdStepInputs = form.querySelectorAll('div[data-step="3"] input[type=radio]');
      this.institutionId = '';
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;

          /** Get chosen categories from Step 1 and put them in array */
          const category_array = [];
          this.$checkboxInputs.forEach(function (element) {
            if (element.checked === true) {
              category_array.push(element.value)
            }
          });

          /** Hidden or visible institutions by category which is display in Step 3*/
          for (let i = 0; i < category_array.length; i++) {
            for (let j = 0; j < this.$catDivs.length; j++) {
              const innerTextArray = this.$catDivs[j].innerText.split('% ');
              if (innerTextArray.indexOf(category_array[i]) > -1) {

                this.$catDivs[j].parentElement.parentElement.parentElement.setAttribute('style', 'display: inline-block')
              }
              else {
                this.$catDivs[j].parentElement.parentElement.parentElement.setAttribute('style', 'display: none')
              }
            }
          }
          // console.log(this.$fifthStepDiv);
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          const category_array = [];
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      /** Get data from inputs and show them in summary */
      const category_array = [];
          this.$checkboxInputs.forEach(function (element) {
            if (element.checked === true) {
              category_array.push(element.value)
            }
          });
      if (this.currentStep === 5) {
        // console.log(this.$fifthStepDiv.querySelectorAll('li')[0].querySelector('span.summary--text').innerText);
        let textLi = this.$fifthStepDiv.querySelectorAll('li');
        textLi[0].querySelector('span.summary--text').innerHTML = this.$bagsInput.value + ' worki zawierające: <br>' + category_array.join(', ');
        this.$divsTitle.forEach(function (element) {
          if (element.parentElement.parentElement.firstChild.nextSibling.checked === true) {
            textLi[1].querySelector('span.summary--text').innerHTML = 'Dla fundacji ' + '"' + element.innerText + '"'
          }
        });
        textLi[2].innerHTML = this.$addressInput.value;
        textLi[3].innerHTML = this.$cityInput.value;
        textLi[4].innerHTML = this.$postcodeInput.value;
        textLi[5].innerHTML = this.$phoneInput.value;
        textLi[6].innerHTML = this.$dateInput.value;
        textLi[7].innerHTML = this.$timeInput.value;
        textLi[8].innerHTML = this.$commentTextarea.value;

        }


    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      // e.preventDefault();
      this.currentStep++;


      const category_array = [];
          this.$checkboxInputs.forEach(function (element) {
            if (element.checked === true) {
              category_array.push(element.value)
            }
          });
      let institutionId = '';
      this.$thirdStepInputs.forEach(function (element) {
          if (element.checked === true) {
            institutionId = element.value

          }
        });

      // $.ajax({
      //   type: "POST",
      //   url: "{% url 'add_donation' %}",
      //   data: {
      //     'quantity': this.$bagsInput.value,
      //     'categories': category_array,
      //     'institution': institutionId,
      //     'address': this.$addressInput,
      //     'phone_number': this.$phoneInput,
      //     'zip_code': this.$postcodeInput,
      //     'pick_up_date': this.$dateInput,
      //     'pick_up_time': this.$timeInput,
      //     'pick_up_comment': this.$postcodeInput,
      //     'user': this.$userId,
      //   },
      //   success: function () {
      //     $('#message').html("<h2>Donation Form Submitted!</h2>")
      //   }
      // });
      // return false;

      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }



});
