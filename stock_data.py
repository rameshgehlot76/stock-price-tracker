import yfinance as yf
import plotly.graph_objects as go

def get_stock_data(symbol):  
    try:
        symbol = symbol.strip().upper() 
        if not symbol:
            return {'error': 'Please enter a stock symbol.'} 
        
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # Check if valid stock 
        if not info or (info.get('currentPrice') is None and info.get('regularMarketPrice') is None ): 
            return {'error ': f'Symbol "{symbol}" not found. Try TCS.NS for Indian stocks and AAPL for US stocks.'}
        
        
        current_price = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        day_high = info.get('dayHigh') or info.get('regularMarketDayHigh') or 'N/A'  
        day_low = info.get('dayLow') or info.get('regularMarketDayLow') or 'N/A' 
        prev_close = info.get('previousClose') or info.get('regularMarketPreviousClose') or 0  
        
        company_name = info.get('longName') or info.get('shortName') or symbol   
        
        # Claculate change % 
        if current_price and prev_close and prev_close != 0: 
            change = round(((current_price - prev_close) / prev_close) * 100, 2) 
            change_abs = round(current_price - prev_close, 2) 
        else:
            change = 0
            change_abs = 0
            
        # Last 30 days history
        history = stock.history(period="1mo") 
        if history.empty:
            return {'error': f'No history found for "{symbol}".'} 
        
        return {
            'name': company_name,  
            'symbol': symbol,
            'price': round(float(current_price), 2), 
            'high': round(float(day_high), 2) if day_high != 'N/A' else 'N/A',
            'low': round(float(day_low), 2) if day_low != 'N/A' else 'N/A',
            'prev_close': round(float(prev_close), 2),  
            'change': change, 
            'change_abs': change_abs,
            'history': history,
            'error': None, 
        } 
    except Exception as e:
        return {'error': f'Something went wrong: {str(e)}'}    
    
    
def create_chart(history, symbol): 
    try:
        fig = go.Figure() 
        
        # Price line 
        fig.add_trace(go.Scatter(
            x=history.index,
            y=history['Close'].round(2), 
            mode='lines',
            name='Close Price',
            line=dict(color='#00C853', width=2.5),
            hovertemplate='<b>%{x|%d %b %Y}</b><br>Price: ₹%{y:,.2f}<extra></extra>'
        ))
        
        # 7-day moving average
        if len(history) >= 7:
            ma7 = history['Close'].rolling(window=7).mean()
            fig.add_trace(go.Scatter(
                x=history.index,
                y=ma7.round(2),
                mode='lines',
                name='7-Day MA',
                line=dict(color='#FFD600', width=1.5, dash='dot'),
                hovertemplate='7-Day MA: ₹%{y:,.2f}<extra></extra>'
            ))
 
        fig.update_layout(
            title=f'{symbol} — 30-Day Price History',
            xaxis_title='Date',
            yaxis_title='Price (₹)',
            paper_bgcolor='#1e1e2e',
            plot_bgcolor='#1e1e2e',
            font=dict(color='white', family='Segoe UI'),
            xaxis=dict(gridcolor='#2a2a3e', linecolor='#444'),
            yaxis=dict(gridcolor='#2a2a3e', linecolor='#444'),
            legend=dict(bgcolor='#2a2a3e', bordercolor='#444', borderwidth=1),
            hovermode='x unified',
            margin=dict(l=10, r=10, t=50, b=10),
            height=400
        )
 
        return fig.to_html(full_html=False, config={'displayModeBar': False})
 
    except Exception as e:
        return f"<p style='color:red'>Chart error: {str(e)}</p>"   
    
    
    
    


