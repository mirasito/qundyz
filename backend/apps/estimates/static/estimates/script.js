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
// ==== функции для динамического добавления/удаления строк и этапов ====

/**
 * Вставляет новую строку работы (по образцу первой).
 */
function addWorkRow(btn) {
  const tbody = btn.closest('.stage-block').querySelector('.works-table tbody');
  const firstRow = tbody.querySelector('tr');
  const newRow = firstRow.cloneNode(true);
  // очистим поля
  newRow.querySelector('.work-name').value = '';
  newRow.querySelector('.work-hours').value = '0';
  newRow.querySelector('.work-cost').value = '0';
  newRow.querySelector('.work-total').textContent = '0 ₸';
  tbody.appendChild(newRow);
  totalRecalc();
}

/**
 * Вставляет новую строку материала.
 */
function addMaterialRow(btn) {
  const tbody = btn.closest('.stage-block').querySelector('.materials-table tbody');
  const firstRow = tbody.querySelector('tr');
  const newRow = firstRow.cloneNode(true);
  newRow.querySelector('.material-name').value = '';
  newRow.querySelector('.material-quantity').value = '0';
  newRow.querySelector('.material-unit').value = '';
  newRow.querySelector('.material-price').value = '0';
  newRow.querySelector('.material-total').textContent = '0 ₸';
  tbody.appendChild(newRow);
  totalRecalc();
}

/**
 * Удаляет строку работы или материала и сразу пересчитывает.
 */
function deleteRow(btn) {
  const tr = btn.closest('tr');
  tr.parentNode.removeChild(tr);
  totalRecalc();
}

/**
 * Удаляет весь этап (карточку) и пересчитывает всю смету.
 */
function deleteStage(btn) {
  const stage = btn.closest('.estimate-stage');
  stage.parentNode.removeChild(stage);
  totalRecalc();
}

/**
 * Пересчитывает все этапы и итоговую сумму.
 */
function totalRecalc() {
  let grandTotal = 0;
  document.querySelectorAll('.estimate-stage').forEach(stage => {
    let stageSum = 0;
    // работы
    stage.querySelectorAll('.works-table tbody tr').forEach(tr => {
      const h = parseFloat(tr.querySelector('.work-hours').value) || 0;
      const c = parseFloat(tr.querySelector('.work-cost').value) || 0;
      const t = h * c;
      tr.querySelector('.work-total').textContent = t.toLocaleString('ru-RU',{minimumFractionDigits:2}) + ' ₸';
      stageSum += t;
    });
    // материалы
    stage.querySelectorAll('.materials-table tbody tr').forEach(tr => {
      const q = parseFloat(tr.querySelector('.material-quantity').value) || 0;
      const p = parseFloat(tr.querySelector('.material-price').value) || 0;
      const t = q * p;
      tr.querySelector('.material-total').textContent = t.toLocaleString('ru-RU',{minimumFractionDigits:2}) + ' ₸';
      stageSum += t;
    });
    // записываем для этапа
    const disp = stage.querySelector('.stage-cost-display');
    disp.textContent = stageSum.toLocaleString('ru-RU',{minimumFractionDigits:2}) + ' ₸';
    stage.querySelector('.stage-cost-input').value = stageSum.toFixed(2);
    grandTotal += stageSum;
  });
  // итоговая сумма
  document.getElementById('total-display').textContent =
    grandTotal.toLocaleString('ru-RU',{minimumFractionDigits:2}) + ' ₸';
  document.getElementById('total-cost').value = grandTotal.toFixed(2);
}

// привязываем пересчет к любому изменению в таблицах
document.body.addEventListener('input', e => {
  if (e.target.closest('.cost-table')) totalRecalc();
});

// выполняем初ичный пересчет при загрузке
document.addEventListener('DOMContentLoaded', totalRecalc);
/**
 * Combined script for estimate detail page.
 * Handles accordion toggles, dynamic row add/remove, auto-textarea grow,
 * emoji icons, and real-time recalculation of stage and total sums.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Auto‑grow for textarea inputs
  document.querySelectorAll('.input--autoGrow').forEach(el => {
    autoGrow(el);
    el.addEventListener('input', () => autoGrow(el));
  });

  // Inject appropriate emoji for each stage
  const emojiMap = [
    [/план/i,        "🗂️"],
    [/демонтаж/i,    "🪚"],
    [/переплан/i,    "🏗️"],
    [/инженер/i,     "🔧"],
    [/чернов/i,      "🧱"],
    [/чистов/i,      "🎨"],
    [/мебел|декор/i, "🛋️"]
  ];
  document.querySelectorAll(".stage-emoji").forEach(span => {
    const title = span.dataset.stage || "";
    const found = emojiMap.find(([re]) => re.test(title));
    span.textContent = found ? found[1] : "📦";
  });

  // Initial total calculation
  totalRecalc();

  // Recalculate whenever any input inside a cost-table changes
  document.body.addEventListener('input', e => {
    if (e.target.closest('.cost-table')) {
      totalRecalc();
    }
  });
});

/**
 * Expand a textarea height to fit its content.
 */
function autoGrow(el) {
  el.style.height = "auto";
  el.style.height = el.scrollHeight + "px";
}

/**
 * Toggle accordion details for a stage.
 */
function toggleStageDetails(id) {
  const details = document.getElementById(`details-${id}`);
  const arrow = document.getElementById(`arrow-${id}`);
  if (!details || !arrow) return;
  const open = details.style.display === "block";
  details.style.display = open ? "none" : "block";
  arrow.textContent = open ? "▼" : "▲";
}

/**
 * Add a new work row by cloning the first existing row.
 */
function addWorkRow(btn) {
  const tbody = btn.closest('.stage-block').querySelector('.works-table tbody');
  const firstRow = tbody.querySelector('tr');
  const newRow = firstRow.cloneNode(true);
  newRow.querySelector('.work-name').value = '';
  newRow.querySelector('.work-hours').value = '0';
  newRow.querySelector('.work-cost').value = '0';
  newRow.querySelector('.work-total').textContent = '0 ₸';
  tbody.appendChild(newRow);
  totalRecalc();
}

/**
 * Add a new material row by cloning the first existing row.
 */
function addMaterialRow(btn) {
  const tbody = btn.closest('.stage-block').querySelector('.materials-table tbody');
  const firstRow = tbody.querySelector('tr');
  const newRow = firstRow.cloneNode(true);
  newRow.querySelector('.material-name').value = '';
  newRow.querySelector('.material-quantity').value = '0';
  newRow.querySelector('.material-unit').value = '';
  newRow.querySelector('.material-price').value = '0';
  newRow.querySelector('.material-total').textContent = '0 ₸';
  tbody.appendChild(newRow);
  totalRecalc();
}

/**
 * Delete a single work or material row and recalculate.
 */
function deleteRow(btn) {
  const tr = btn.closest('tr');
  if (tr) {
    tr.remove();
    totalRecalc();
  }
}

/**
 * Delete an entire stage card and recalculate total.
 */
function deleteStage(btn) {
  const stage = btn.closest('.estimate-stage');
  if (stage) {
    stage.remove();
    totalRecalc();
  }
}

/**
 * Recalculate each stage sum and the grand total.
 */
function totalRecalc() {
  let grandTotal = 0;
  document.querySelectorAll('.estimate-stage').forEach(stage => {
    let stageSum = 0;

    // Sum works
    stage.querySelectorAll('.works-table tbody tr').forEach(tr => {
      const h = parseFloat(tr.querySelector('.work-hours').value) || 0;
      const c = parseFloat(tr.querySelector('.work-cost').value) || 0;
      const t = h * c;
      tr.querySelector('.work-total').textContent = t.toLocaleString('ru-RU', { minimumFractionDigits: 2 }) + ' ₸';
      stageSum += t;
    });

    // Sum materials
    stage.querySelectorAll('.materials-table tbody tr').forEach(tr => {
      const q = parseFloat(tr.querySelector('.material-quantity').value) || 0;
      const p = parseFloat(tr.querySelector('.material-price').value) || 0;
      const t = q * p;
      tr.querySelector('.material-total').textContent = t.toLocaleString('ru-RU', { minimumFractionDigits: 2 }) + ' ₸';
      stageSum += t;
    });

    // Update stage display and hidden input
    stage.querySelector('.stage-cost-display').textContent = stageSum.toLocaleString('ru-RU', { minimumFractionDigits: 2 }) + ' ₸';
    const hiddenInput = stage.querySelector('.stage-cost-input');
    if (hiddenInput) hiddenInput.value = stageSum.toFixed(2);

    grandTotal += stageSum;
  });

  // Update grand total display and hidden input
  const totalDisplay = document.getElementById('total-display');
  if (totalDisplay) {
    totalDisplay.textContent = grandTotal.toLocaleString('ru-RU', { minimumFractionDigits: 2 }) + ' ₸';
  }
  const totalInput = document.getElementById('total-cost');
  if (totalInput) {
    totalInput.value = grandTotal.toFixed(2);
  }
}