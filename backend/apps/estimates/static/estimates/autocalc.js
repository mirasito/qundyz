document.addEventListener("DOMContentLoaded", () => {
  const NF     = new Intl.NumberFormat("ru‑RU",{minimumFractionDigits:2,maximumFractionDigits:2});
  const safe   = v => isNaN(parseFloat(v)) ? 0 : parseFloat(v);
  const money  = v => NF.format(v) + " ₸";

  /* маленькая помощница: форматируем input, но “сырое” число
     храним в data‑атрибуте, чтобы последующие safe(..) работали */
  const pretty = inp => {
    const raw = safe(inp.value);
    inp.dataset.raw = raw;          // сохраняем
    inp.value = NF.format(raw);     // показываем
    return raw;
  };

  function rowTotal(tr){
    // материал
    if (tr.closest(".materials-table")){
      const qty   = safe(tr.querySelector(".material-quantity").value);
      const price = pretty(tr.querySelector(".material-price"));
      return qty * price;
    }
    // работа
    const vol  = safe(tr.querySelector(".work-hours").value);
    const rate = pretty(tr.querySelector(".work-cost"));
    return vol * rate;
  }

  function stageRecalc(stage){
    let sum = 0;
    stage.querySelectorAll("tbody tr").forEach(tr=>{
      const t = rowTotal(tr);
      tr.querySelector(".material-total, .work-total").textContent = money(t);
      sum += t;
    });
    stage.querySelector(".stage-cost-display").textContent = money(sum);
    stage.querySelector(".stage-summary strong").textContent = money(sum);
    stage.querySelector(".stage-cost-input").value = sum.toFixed(2);
    return sum;
  }

  function totalRecalc(){
    let total = 0;
    document.querySelectorAll(".estimate-stage").forEach(s=> total += stageRecalc(s));
    document.getElementById("total-cost").value        = total.toFixed(2);
    document.getElementById("total-display").textContent = money(total);
  }

  document.body.addEventListener("input", e=>{
    if (e.target.closest(".cost-table")) totalRecalc();
  });

  /* ––‑  остальной Ваш код (addRow / deleteRow / …) не трогаем ‑–– */

  totalRecalc();            // первый расчёт
});