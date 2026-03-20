from agent import BrowserAgent

def run():
    agent = BrowserAgent()

    try:
        agent.open_page("https://medium.com/@malipodendro")
        agent.scan_page()           
        agent.detect_hidden_elements()
        agent.llm_scan()              
        agent.safe_click("text=Sign in")
        agent.compare_detection()      

    finally:
        input("Press Enter to close...")
        agent.close()

if __name__ == "__main__":
    run()