function combineEducationInputs() {
    var combinedInput = document.getElementById('education');
    var combinedInput1 = document.getElementById('educations');

    var collegeName = document.getElementById('college-name').value;
    var graduation = document.getElementById('graduation').value;
    var year = document.getElementById('year').value;
    var percentage = document.getElementById('percentage').value;

    if (collegeName && graduation && year && percentage) {
        combinedInput.innerHTML += collegeName + ", " + graduation + ", " + year + ", " + percentage + "<br>";
    }
    if (collegeName && graduation && year && percentage) {
        combinedInput1.value += collegeName + "," + graduation + "," + year + "," + percentage + "|";
    }

    toggleAddEducationModal();
}

function toggleAddEducationModal() {
    var modal = document.getElementById('add-education-modal');

    document.getElementById('college-name').value = '';
    document.getElementById('graduation').value = '';
    document.getElementById('year').value = '';
    document.getElementById('percentage').value = '';

    if (modal.style.display === "block") {
        modal.style.display = "none";
    }
    else {
        modal.style.display = "block";
    }
}

function combineSkillInputs() {
    var combinedInput1 = document.getElementById('skill');
     var combinedInput2 = document.getElementById('skills');

    var skill = document.getElementById('skill-name').value;


        combinedInput1.innerText += skill+"<br>";
        combinedInput2.value+=skill+"|";

    toggleAddSkillModal();
}

function toggleAddSkillModal() {
    var modal = document.getElementById('add-skill-modal');

    document.getElementById('skill-name').value = '';

    if (modal.style.display === "block") {
        modal.style.display = "none";
    }
    else {
        modal.style.display = "block";
    }
}

function combineExperienceInputs() {
    var combinedInput2 = document.getElementById('experience');
    var combinedInput3 = document.getElementById('experiences');

    var workplace = document.getElementById('work-place').value;
    var duration = document.getElementById('duration').value;

    if (workplace && duration) {
        combinedInput2.innerHTML += workplace + ", " + duration +  "<br>";
    }
    if (workplace && duration) {
        combinedInput3.value += workplace + "," + duration +  "|";
    }

    toggleAddExperienceModal();
}

function toggleAddExperienceModal() {
    var modal = document.getElementById('add-experience-modal');
    var searchBox = new google.maps.places.SearchBox(document.getElementById('work-place'));

    document.getElementById('work-place').value = '';
    document.getElementById('duration').value = '';

    if (modal.style.display === "block") {
        modal.style.display = "none";
    }
    else {
        modal.style.display = "block";
    }
}


function combineTrainInputs() {
    var combinedInput1 = document.getElementById('train');
     var combinedInput2 = document.getElementById('train1');

    var train = document.getElementById('train-place').value;


        combinedInput1.InnerText += train+" <br>";
        combinedInput2.value+=train+"|";

    toggleAddTrainModal();
}

function toggleAddTrainModal() {
    var modal = document.getElementById('add-train-modal');

    document.getElementById('train-place').value = '';

    if (modal.style.display === "block") {
        modal.style.display = "none";
    }
    else {
        modal.style.display = "block";
    }
}