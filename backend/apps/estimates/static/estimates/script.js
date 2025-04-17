/**
 * Показывает экран с определённым номером (1, 2 или 3).
 * Скрывает все остальные.
 */
function goToScreen(screenNumber) {
  const screens = document.querySelectorAll(".screen");
  screens.forEach(screen => {
    screen.classList.remove("active");
  });
  const target = document.getElementById(`screen-${screenNumber}`);
  if (target) {
    target.classList.add("active");
  }
}

function toggleStageDetails(id) {
  const details = document.getElementById(`details-${id}`);
  const arrow = document.getElementById(`arrow-${id}`);
  if (!details || !arrow) return;
  
  if (details.style.display === "none" || details.style.display === "") {
    details.style.display = "block";
    arrow.textContent = "▲";
  } else {
    details.style.display = "none";
    arrow.textContent = "▼";
  }
}

function openAddStageModal() {
  document.getElementById('addStageModal').style.display = 'block';
}

function closeAddStageModal() {
  document.getElementById('addStageModal').style.display = 'none';
}

function addStage(event) {
  event.preventDefault();
  const sname = document.getElementById('stage-name').value;
  const sduration = document.getElementById('stage-duration').value;
  const scost = document.getElementById('stage-cost').value;
  alert(`Этап добавлен: ${sname} (Длительность: ${sduration} дн, Стоимость: ${scost} ₸)`);
  closeAddStageModal();
  return false;
}

// Открывает форму добавления материала
function openMaterialForm(stageIndex) {
  // stageIndex передается как forloop.counter0, поэтому прибавляем 1
  document.getElementById('material-stage-index').value = parseInt(stageIndex, 10);
  document.getElementById('materialModal').style.display = 'block';
}

// Закрывает форму добавления материала
function closeMaterialForm() {
  document.getElementById('materialModal').style.display = 'none';
}

// Аналогично для работ
function openWorkForm(stageIndex) {
  document.getElementById('work-stage-index').value = parseInt(stageIndex, 10);
  document.getElementById('workModal').style.display = 'block';
}

function closeWorkForm() {
  document.getElementById('workModal').style.display = 'none';
}

// Добавление материала (локальный пример)
function addMaterial(event) {
  event.preventDefault();
  const stageIndex0 = document.getElementById('material-stage-index').value;
  // Переводим forloop.counter0 в forloop.counter, прибавляя 1
  const stageIndex = parseInt(stageIndex0, 10) + 1;
  const name = document.getElementById('material-name').value;
  const qty = parseFloat(document.getElementById('material-quantity').value);
  const unit = document.getElementById('material-unit').value;
  const price = parseFloat(document.getElementById('material-price').value);
  const total = qty * price;

  // Поиск таблицы материалов для данного этапа по селектору
  const tableBody = document.querySelector(`#details-${stageIndex} .materials-table tbody`);

  if (tableBody) {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${name}</td>
        <td>${qty.toFixed(2)}</td>
        <td>${unit}</td>
        <td>${price.toFixed(2)} ₸</td>
        <td><strong>${total.toFixed(2)} ₸</strong></td>
      `;
      tableBody.appendChild(tr);
      alert(`Добавлен материал: ${name}, сумма = ${total.toFixed(2)} ₸`);
  } else {
      alert('Не найдена таблица материалов для этапа index=' + stageIndex);
  }
  closeMaterialForm();
  return false;
}

// Добавление работы (локальный пример)
function addWork(event) {
  event.preventDefault();
  const stageIndex0 = document.getElementById('work-stage-index').value;
  // Преобразуем to integer и прибавляем 1, так как id деталей этапа формируется как details-{{ forloop.counter }}
  const stageIndex = parseInt(stageIndex0, 10) + 1;
  const wname = document.getElementById('work-name').value;
  const whours = parseFloat(document.getElementById('work-hours').value);
  const wcost = parseFloat(document.getElementById('work-cost').value);
  const wtotal = whours * wcost;
  
  // Ищем таблицу работ по селектору
  const tableBody = document.querySelector(`#details-${stageIndex} .works-table tbody`);
  
  if (tableBody) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${wname}</td>
      <td>${whours.toFixed(2)}</td>
      <td>${wcost.toFixed(2)} ₸</td>
      <td><strong>${wtotal.toFixed(2)} ₸</strong></td>
    `;
    tableBody.appendChild(tr);
    alert(`Добавлена работа: ${wname}, сумма = ${wtotal.toFixed(2)} ₸`);
  } else {
    alert('Не найдена таблица работ для этапа index=' + stageIndex);
  }
  
  closeWorkForm();
  return false;
}