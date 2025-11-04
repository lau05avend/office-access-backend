document.addEventListener("DOMContentLoaded", () => {
  const q = (id) => document.getElementById(id);
  const ui = {
    form: q("visitanteForm"),
    tipo: q("tipo_visitante"),
    empresa: q("empresa_field"),
    toast: q("toast"),
    btn: q("submitBtn"),
    text: document.querySelector(".btn-text"),
    spinner: document.querySelector(".spinner"),
  };

  ui.tipo.addEventListener("change", () =>
    ui.empresa.classList.toggle("hidden", ui.tipo.value !== "1"),
  );

  ui.form.addEventListener("submit", async (e) => {
    e.preventDefault();
    toggle(true);

    const d = (id) => q(id).value.trim();
    const body = {
      numero_identificacion: d("numero_identificacion"),
      tipo_identificacion: d("tipo_identificacion"),
      nombres: d("nombres"),
      apellidos: d("apellidos"),
      tipo_visitante: ui.tipo.value === "1" ? "Empresarial" : "Personal",
      empresa_representa: d("empresa_representa") || null,
    };

    try {
      const res = await fetch("http://localhost:5000/api/visitantes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await res.json();

      if (res.ok && data.status === "success") {
        showToast(`✅ ${data.message}`);
        ui.form.reset();
        ui.empresa.classList.add("hidden");
      } else {
        const msg = data.error || data.message || "Error desconocido.";
        showToast(`❌ ${msg}`, true);
      }
    } catch (err) {
      console.error(err);
      showToast("❌ Error de conexión con el servidor.", true);
    } finally {
      toggle(false);
    }
  });

  const toggle = (s) => {
    ui.btn.disabled = s;
    ui.text.textContent = s ? "Cargando..." : "Registrar";
    ui.spinner.classList.toggle("hidden", !s);
  };

  const showToast = (m, e = false) => {
    ui.toast.textContent = m;
    ui.toast.className = `toast show ${e ? "error" : ""}`;
    setTimeout(() => ui.toast.classList.remove("show"), 3500);
  };
});
