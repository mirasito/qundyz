/* =======  Автопересчёт сметы  ======= */
document.addEventListener("DOMContentLoaded", () => {

  /* ---------- утилиты ---------- */
  const nf     = new Intl.NumberFormat("ru-RU",
                 { minimumFractionDigits:2, maximumFractionDigits:2 });
  const money  = v => nf.format(v) + " ₸";                 // узкий NBSP перед ₸
  const num    = v => parseFloat(String(v)
                     .replace(/\s| /g,"")      // убираем пробелы и NBSP
                     .replace(",",".")) || 0;  // заменяем запятую на точку

  /* ---------- строка ---------- */
  function rowSum(tr){
    if (tr.closest(".materials-table")) {                  // материал
      const qty   = num(tr.querySelector(".material-quantity").value);
      const price = num(tr.querySelector(".material-price").value);
      const t = qty * price;
      tr.querySelector(".material-total").textContent = money(t);
      return t;
    }                                                      // работа
    const vol  = num(tr.querySelector(".work-hours").value);
    const rate = num(tr.querySelector(".work-cost").value);
    const t    = vol * rate;
    tr.querySelector(".work-total").textContent = money(t);
    return t;
  }

  /* ---------- этап ---------- */
  function stageSum(stage){
    let sum = 0;
    stage.querySelectorAll("tbody tr").forEach(tr => sum += rowSum(tr));

    // вывод
    stage.querySelector(".stage-cost-display").textContent   = money(sum);
    stage.querySelector(".stage-summary  strong").textContent= money(sum);
    stage.querySelector(".stage-cost-input").value           = sum.toFixed(2);
    return sum;
  }

  /* ---------- вся смета ---------- */
  function estimateSum(){
    let total = 0;
    document.querySelectorAll(".estimate-stage")
            .forEach(s => total += stageSum(s));

    document.getElementById("total-cost").value          = total.toFixed(2);
    document.getElementById("total-display").textContent = money(total);
  }

  /* ---------- слушаем любые изменения в таблицах ---------- */
  document.body.addEventListener("input",  e=>{
    if (e.target.closest(".cost-table")) estimateSum();
  });
  document.body.addEventListener("change", e=>{
    if (e.target.closest(".cost-table")) estimateSum();
  });

  /* первый пересчёт после загрузки */
  estimateSum();
});