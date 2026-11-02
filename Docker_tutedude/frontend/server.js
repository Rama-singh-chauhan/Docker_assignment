/**
 * Express Frontend
 * ----------------
 * Serves the registration form and forwards submissions to the Flask backend.
 *
 * Inside Docker Compose the backend is reachable by its service name
 * ("backend"), so BACKEND_URL defaults to http://backend:5000.
 */
const express = require("express");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;
const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:5000";

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// Show the form
app.get("/", (req, res) => {
  res.render("index", { errors: [], values: {} });
});

// Handle the form: send the data to Flask and render the result
app.post("/submit", async (req, res) => {
  const formData = {
    name: req.body.name,
    email: req.body.email,
    age: req.body.age,
    course: req.body.course,
    message: req.body.message,
  };

  try {
    const response = await fetch(`${BACKEND_URL}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
    const result = await response.json();

    if (!response.ok || !result.success) {
      return res
        .status(response.status)
        .render("index", { errors: result.errors || ["Submission failed."], values: formData });
    }

    res.render("success", { message: result.message, data: result.data });
  } catch (err) {
    console.error("Backend request failed:", err.message);
    res.status(502).render("index", {
      errors: [`Could not reach the backend at ${BACKEND_URL}. Is the Flask service running?`],
      values: formData,
    });
  }
});

// Health check for Docker
app.get("/health", (req, res) => res.json({ status: "ok" }));

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Frontend running on http://localhost:${PORT}`);
  console.log(`Forwarding form submissions to ${BACKEND_URL}`);
});
