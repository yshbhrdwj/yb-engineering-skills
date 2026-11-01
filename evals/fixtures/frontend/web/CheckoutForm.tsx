import "./checkout.css";

type Props = { errors: string[]; onSubmit: () => void; showCvcHelp: () => void };

export function CheckoutForm({ errors, onSubmit, showCvcHelp }: Props) {
  return (
    <form onSubmit={(e) => { e.preventDefault(); onSubmit(); }} noValidate>
      <h2 id="error-summary" tabIndex={-1} className={errors.length ? "" : "visually-hidden"}>
        {errors.length ? `${errors.length} problems need attention` : ""}
      </h2>

      <label className="visually-hidden" htmlFor="card-name">Name on card</label>
      <input id="card-name" placeholder="Name on card" autoComplete="cc-name" />

      <input id="card-number" placeholder="Card number" inputMode="numeric" autoComplete="cc-number" />
      {errors.includes("card-number") && <span className="error">Enter a valid card number</span>}

      <div className="row">
        <label htmlFor="expiry">Expiry (MM/YY)</label>
        <input id="expiry" autoComplete="cc-exp" />
        <button type="button" className="icon-button" onClick={showCvcHelp}>
          <svg aria-hidden="true" width="16" height="16" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" /></svg>
        </button>
      </div>

      <div className="terms">
        <input type="checkbox" id="terms" />
        <span>I agree to the terms</span>
      </div>

      <div className="pay-button" onClick={onSubmit}>Pay $48.00</div>
      <p className="fine-print">Charged in USD. Your bank may add fees.</p>
    </form>
  );
}
