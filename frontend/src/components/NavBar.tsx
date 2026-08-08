import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Vue d'ensemble", end: true },
  { to: "/indicators", label: "Indicateurs", end: false },
  { to: "/alerts", label: "Alertes", end: false },
];

function NavBar() {
  return (
    <nav className="flex gap-1 mb-8 border-b border-border-subtle">
      {links.map((link) => (
        <NavLink
          key={link.to}
          to={link.to}
          end={link.end}
          className={({ isActive }) =>
            `px-4 py-2.5 font-mono text-xs uppercase tracking-widest border-b-2 transition-colors ${
              isActive
                ? "border-signal text-signal"
                : "border-transparent text-text-muted hover:text-text-primary"
            }`
          }
        >
          {link.label}
        </NavLink>
      ))}
    </nav>
  );
}

export default NavBar;