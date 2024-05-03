const search_button = document.querySelector(".search_button");
const input_search = document.querySelector(".input_search");
search_button.addEventListener("click", function (e) {
  e.preventDefault();
  console.log(input_search.value);
});
