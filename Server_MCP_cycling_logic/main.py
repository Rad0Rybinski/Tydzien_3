from mcp.server.fastmcp import FastMCP

mcp = FastMCP("cycling_logic")

@mcp.tool()
async def analyze_fatigue_and_power(avg_heart_rate: float, max_heart_rate: int, rpe: int, current_power: float):
    """
    Analizuje zmęczenie i decyduje, czy można zwiększyć wysiłek o 2%.
    avg_heart_rate: średnie tętno z treningu
    max_heart_rate: Twoje tętno maksymalne
    rpe: skala zmęczenia 1-10 (Rating of Perceived Exertion)
    current_power: aktualna moc w watach
    """
    hr_intensity = avg_heart_rate / max_heart_rate
    
    
    if hr_intensity < 0.75 and rpe < 6:
        new_power = current_power * 1.02
        status = "ORGANIZM GOTOWY"
        recommendation = f"Twoje tętno jest niskie w stosunku do wysiłku. Możesz zwiększyć moc o 2% do poziomu {new_power:.1f} W."
        can_increase = True
    elif rpe >= 8:
        status = "WYKRYTO ZMĘCZENIE"
        recommendation = "Wysokie poczucie zmęczenia. Pozostań przy obecnej mocy lub zaplanuj regenerację."
        can_increase = False
    else:
        status = "STABILNIE"
        recommendation = "Parametry w normie. Kontynuuj plan bez zmian."
        can_increase = False

    return {
        "status": status,
        "recommendation": recommendation,
        "metrics": {
            "hr_intensity_percent": f"{hr_intensity*100:.1f}%",
            "suggested_power": f"{current_power * 1.02 if can_increase else current_power:.1f} W"
        }
    }

@mcp.tool()
async def compare_with_pro_stats(pro_stats_text: str, user_weight: float, user_ftp: float):
    """
    Porównuje Twoje dane z danymi zawodowca (skopiowanymi z ProCyclingStats).
    """
    
    return {
        "instruction": "Przeanalizuj powyższe dane zawodowca i porównaj je z wagą użytkownika ({user_weight} kg) oraz FTP ({user_ftp} W). Wyciągnij wnioski dotyczące stosunku W/kg.",
        "data_received": pro_stats_text[:100] + "..."
    }

if __name__ == "__main__":
    mcp.run(transport='stdio')