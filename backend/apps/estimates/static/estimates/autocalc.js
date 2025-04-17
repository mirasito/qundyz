document.addEventListener("DOMContentLoaded", function () {
    function parseFloatSafe(value) {
      const parsed = parseFloat(value);
      return isNaN(parsed) ? 0 : parsed;
    }
  
    function updateMaterialCost(row) {
      const qty = parseFloatSafe(row.querySelector('[name$="_quantity"]').value);
      const price = parseFloatSafe(row.querySelector('[name$="_price_per_unit"]').value);
      const total = qty * price;
      row.querySelector(".material-total").textContent = `${total.toFixed(2)} ₸`;
      return total;
    }
  
    function updateWorkCost(row) {
      const hours = parseFloatSafe(row.querySelector('[name$="_hours"]').value);
      const rate = parseFloatSafe(row.querySelector('[name$="_cost_per_hour"]').value);
      const total = hours * rate;
      row.querySelector(".work-total").textContent = `${total.toFixed(2)} ₸`;
      return total;
    }
  
    function updateStageCost(stageElem) {
      let stageTotal = 0;
  
      stageElem.querySelectorAll(".materials-table tbody tr").forEach(row => {
        stageTotal += updateMaterialCost(row);
      });
  
      stageElem.querySelectorAll(".works-table tbody tr").forEach(row => {
        stageTotal += updateWorkCost(row);
      });
  
      const stageCostInput = stageElem.querySelector('.stage-cost input');
      if (stageCostInput) {
        stageCostInput.value = stageTotal.toFixed(2);
      }
  
      stageElem.querySelector(".stage-summary strong").textContent = `${stageTotal.toFixed(2)} ₸`;
      return stageTotal;
    }
  
    function updateTotalEstimate() {
      let estimateTotal = 0;
      document.querySelectorAll(".estimate-stage").forEach(stage => {
        estimateTotal += updateStageCost(stage);
      });
  
      const totalField = document.querySelector('input[name="total_cost"]');
      if (totalField) {
        totalField.value = estimateTotal.toFixed(2);
      }
  
      document.querySelector(".estimate-amount input").value = estimateTotal.toFixed(2);
    }
  
    document.querySelectorAll(".materials-table input, .works-table input").forEach(input => {
      input.addEventListener("input", updateTotalEstimate);
    });
  
    updateTotalEstimate(); // начальный пересчёт
  });