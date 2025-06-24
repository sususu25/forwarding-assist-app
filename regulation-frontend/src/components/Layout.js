import { Link, Outlet, useLocation } from "react-router-dom";
import "./Layout.css";

export default function Layout() {
  const { pathname } = useLocation();

  return (
    <div className="wrapper">
      <aside className="sidebar">
        <h1 className="logo" onClick={() => (window.location.href = "/")}>
          Forwarding DB
        </h1>

        <nav className="menu">
          <Link to="/"       className={pathname==="/"       ? "active":""}>Check Regulations</Link>
          <Link to="/docs"   className={pathname==="/docs"   ? "active":""}>Doc Generator</Link>
          <Link to="/settings" className={pathname==="/settings" ? "active":""}>Settings</Link>
        </nav>

        <img src="/assets/bg-sidebar.png" className="side-img" alt="" />
      </aside>

      <main className="main-area">
        <Outlet />
      </main>
    </div>
  );
}
