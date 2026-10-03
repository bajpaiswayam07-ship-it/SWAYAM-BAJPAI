# ==============================================================================
# StructLab : Stack & Circular Queue CLI Suite (Interactive Terminal App)
# Optimized for Windows Command Prompt (CMD) & PowerShell
# ==============================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "StructLab - Stack and Circular Queue CLI"

function Play-Beep($type) {
    try {
        switch ($type) {
            "push"    { [Console]::Beep(520, 100) }
            "pop"     { [Console]::Beep(380, 100) }
            "enqueue" { [Console]::Beep(640, 110) }
            "dequeue" { [Console]::Beep(440, 110) }
            "peek"    { [Console]::Beep(880, 120) }
            "error"   { [Console]::Beep(220, 200) }
            "success" { [Console]::Beep(523, 80); [Console]::Beep(659, 80); [Console]::Beep(784, 120) }
            "hacker"  {
                # Cyber hacker terminal frequency sweep
                $matrixNotes = @(440, 880, 620, 1240, 1860, 930, 1400, 2100, 1600, 2400, 3000)
                foreach ($f in $matrixNotes) {
                    [Console]::Beep($f, 35)
                }
            }
        }
    } catch {}
}

# Global State
$script:StackCapacity = 6
$script:StackItems = [System.Collections.Generic.List[PSCustomObject]]::new()
$script:StackBaseAddr = 0x7FFE00

$script:CQCapacity = 6
$script:CQArray = [string[]]::new($script:CQCapacity)
$script:CQFront = -1
$script:CQRear = -1
$script:CQCount = 0

function Show-HackerIntro {
    Clear-Host
    Write-Host "`n  [+] ESTABLISHING SECURE QUANTUM LINK..." -ForegroundColor Green
    Start-Sleep -Milliseconds 200
    Write-Host "  [+] DECRYPTING ROOT ACCESS PERMISSIONS..." -ForegroundColor DarkGreen
    Start-Sleep -Milliseconds 200
    Play-Beep "hacker"

    Write-Host @"

  ===========================================================================
  ███████╗██╗    ██╗ █████╗ ██╗   ██╗ █████╗ ███╗   ███╗
  ██╔════╝██║    ██║██╔══██╗╚██╗ ██╔╝██╔══██╗████╗ ████║
  ███████╗██║ █╗ ██║███████║ ╚████╔╝ ███████║██╔████╔██║
  ╚════██║██║███╗██║██╔══██║  ╚██╔╝  ██╔══██║██║╚██╔╝██║
  ███████║╚███╔███╔╝██║  ██║   ██║   ██║  ██║██║ ╚═╝ ██║
  ╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝
              B   A   J   P   A   I
  ===========================================================================
"@ -ForegroundColor Green

    Write-Host "  >>> LEAD DEVELOPER & ARCHITECT : " -NoNewline -ForegroundColor White
    Write-Host "SWAYAM BAJPAI" -ForegroundColor Yellow -NoNewline
    Write-Host " <<<" -ForegroundColor White
    Write-Host "  >>> SYSTEM STATUS              : " -NoNewline -ForegroundColor White
    Write-Host "ACCESS GRANTED [ROOT@CYBER]" -ForegroundColor Cyan -NoNewline
    Write-Host " <<<`n" -ForegroundColor White
    Start-Sleep -Milliseconds 900
}

function Clear-ScreenHeader {
    Clear-Host
    Write-Host "===========================================================================" -ForegroundColor DarkGreen
    Write-Host " STRUCTLAB : STACK & CIRCULAR QUEUE" -ForegroundColor Green -NoNewline
    Write-Host " | " -ForegroundColor DarkGray -NoNewline
    Write-Host "DEVELOPER: SWAYAM BAJPAI" -ForegroundColor Yellow
    Write-Host "===========================================================================" -ForegroundColor DarkGreen
}

# ==============================================================================
# STACK (LIFO) FUNCTIONS
# ==============================================================================

function Draw-StackVisual {
    Write-Host "`n  --- STACK VISUAL REPRESENTATION (LIFO) ---" -ForegroundColor Yellow
    Write-Host "  Capacity: " -NoNewline
    Write-Host "$($script:StackItems.Count) / $script:StackCapacity" -ForegroundColor Cyan -NoNewline
    
    if ($script:StackItems.Count -eq 0) {
        Write-Host "  [Status: EMPTY (top = -1)]" -ForegroundColor DarkGray
    } elseif ($script:StackItems.Count -eq $script:StackCapacity) {
        Write-Host "  [Status: FULL (OVERFLOW!)]" -ForegroundColor Red
    } else {
        Write-Host "  [Status: ACTIVE (top = $($script:StackItems.Count - 1))]" -ForegroundColor Green
    }

    Write-Host "`n       +-------------------------------------+" -ForegroundColor DarkGray
    Write-Host "  TOP  | [OPEN TOP - Push & Pop occur here]  |" -ForegroundColor DarkCyan
    Write-Host "       +-------------------------------------+" -ForegroundColor DarkGray

    for ($i = $script:StackCapacity - 1; $i -ge 0; $i--) {
        $addr = "0x" + ($script:StackBaseAddr + $i * 4).ToString("X6")
        if ($i -lt $script:StackItems.Count) {
            $val = $script:StackItems[$i].Value
            $isTop = ($i -eq ($script:StackItems.Count - 1))
            if ($isTop) {
                Write-Host ("  [{0}]  " -f $i) -ForegroundColor Yellow -NoNewline
                Write-Host "| " -ForegroundColor DarkGray -NoNewline
                Write-Host ("{0,-10}" -f $val) -ForegroundColor Yellow -NoNewline
                Write-Host " <-- TOP (Current) " -ForegroundColor Cyan -NoNewline
                Write-Host ("[{0}]" -f $addr) -ForegroundColor DarkGray -NoNewline
                Write-Host " |" -ForegroundColor DarkGray
            } else {
                Write-Host ("  [{0}]  " -f $i) -ForegroundColor DarkGray -NoNewline
                Write-Host "| " -ForegroundColor DarkGray -NoNewline
                Write-Host ("{0,-10}" -f $val) -ForegroundColor White -NoNewline
                Write-Host "                   " -NoNewline
                Write-Host ("[{0}]" -f $addr) -ForegroundColor DarkGray -NoNewline
                Write-Host " |" -ForegroundColor DarkGray
            }
        } else {
            Write-Host ("  [{0}]  " -f $i) -ForegroundColor DarkGray -NoNewline
            Write-Host "| " -ForegroundColor DarkGray -NoNewline
            Write-Host "--- Empty Slot --- " -ForegroundColor DarkGray -NoNewline
            Write-Host ("        [{0}]" -f $addr) -ForegroundColor DarkGray -NoNewline
            Write-Host " |" -ForegroundColor DarkGray
        }
        if ($i -gt 0) {
            Write-Host "       +-------------------------------------+" -ForegroundColor DarkGray
        }
    }
    Write-Host "       +=====================================+" -ForegroundColor DarkCyan
    Write-Host "       |       STACK BASE (Index: 0)         |" -ForegroundColor DarkCyan
    Write-Host "       +=====================================+" -ForegroundColor DarkCyan
}

function Perform-StackPush {
    Write-Host "`n  ===========================================================================" -ForegroundColor DarkCyan
    Write-Host "                    STACK PUSH() OPERATION (LIFO)" -ForegroundColor Yellow
    Write-Host "  ===========================================================================" -ForegroundColor DarkCyan

    if ($script:StackItems.Count -ge $script:StackCapacity) {
        Play-Beep "error"
        Write-Host "`n  [!] STACK OVERFLOW ERROR: Cannot Push! Stack is Full ($($script:StackCapacity) / $($script:StackCapacity))." -ForegroundColor Red
        Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray
        Write-Host "  * Condition: top == capacity - 1 ($($script:StackCapacity - 1) == $($script:StackCapacity - 1))." -ForegroundColor DarkGray
        Write-Host "  * Solution : Pehle Pop() [Option 2] karein ya Capacity badhayein [Option 6]!" -ForegroundColor Yellow
        Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray
        Read-Host "  Press Enter to return to Stack visualizer"
        return
    }

    $val = Read-Host "  Enter value to push (e.g. 42, 99, Alpha)"
    if ([string]::IsNullOrWhiteSpace($val)) { $val = (Get-Random -Minimum 10 -Maximum 99).ToString() }

    $topIdx = $script:StackItems.Count
    $addr = "0x" + ($script:StackBaseAddr + $topIdx * 4).ToString("X6")

    Write-Host "`n  Step 1: Incrementing TOP pointer: [$($topIdx - 1)] ---> [$topIdx]..." -ForegroundColor Cyan
    Start-Sleep -Milliseconds 250

    Write-Host "  Step 2: Writing '$val' at memory slot [$topIdx] ($addr)..." -ForegroundColor Yellow
    $script:StackItems.Add([PSCustomObject]@{ Value = $val; Address = $addr })
    Play-Beep "push"
    Start-Sleep -Milliseconds 250

    Write-Host "`n  +=========================================================================+" -ForegroundColor Green
    Write-Host ("  | [SUCCESS] PUSH COMPLETED: Placed '{0}' at Index [{1}] ({2})  |" -f $val, $topIdx, $addr) -ForegroundColor Green
    Write-Host ("  | [STATUS]  Stack Count: {0}/{1} | TOP pointer is now [{2}]                   |" -f $script:StackItems.Count, $script:StackCapacity, $topIdx) -ForegroundColor Cyan
    Write-Host "  +=========================================================================+" -ForegroundColor Green

    Write-Host ""
    Read-Host "  Press Enter to return to Stack visualizer"
}

function Perform-StackPop {
    Write-Host "`n  ===========================================================================" -ForegroundColor DarkCyan
    Write-Host "                    STACK POP() OPERATION (LIFO)" -ForegroundColor Yellow
    Write-Host "  ===========================================================================" -ForegroundColor DarkCyan

    if ($script:StackItems.Count -eq 0) {
        Play-Beep "error"
        Write-Host "`n  [!] STACK UNDERFLOW ERROR: Cannot Pop from an Empty Stack!" -ForegroundColor Red
        Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray
        Write-Host "  * Rule       : LIFO (Last-In, First-Out) require karta hai ki stack me kam se kam 1 item ho." -ForegroundColor White
        Write-Host "  * Condition  : top == -1 (Stack memory is completely empty)." -ForegroundColor DarkGray
        Write-Host "  * Reason     : Pop hamesha top element ko remove karta hai, par abhi stack EMPTY hai!" -ForegroundColor Yellow
        Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray
        Write-Host "  Pop karne ke liye Stack me pehle element hona zaroori hai!`n" -ForegroundColor Yellow
        Write-Host "  Kya aap abhi Stack me element PUSH karna chahte hain?" -ForegroundColor Cyan
        Write-Host "  [1] Enter a value to PUSH right now" -ForegroundColor Green
        Write-Host "  [2] Auto-fill 3 sample elements (10, 20, 30)" -ForegroundColor Yellow
        Write-Host "  [0] Skip and return to Stack Menu" -ForegroundColor DarkGray
        Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray
        $choice = Read-Host "  Select an option [1, 2, or 0]"

        if ($choice -eq "1") {
            $val = Read-Host "  Enter value to push"
            if ([string]::IsNullOrWhiteSpace($val)) { $val = (Get-Random -Minimum 10 -Maximum 99).ToString() }
            $topIdx = $script:StackItems.Count
            $addr = "0x" + ($script:StackBaseAddr + $topIdx * 4).ToString("X6")
            $script:StackItems.Add([PSCustomObject]@{ Value = $val; Address = $addr })
            Play-Beep "push"
            Write-Host "`n  [SUCCESS] Value '$val' Pushed! New TOP is now [$topIdx]. Ab aap Pop() test kar sakte hain!" -ForegroundColor Green
            Start-Sleep -Milliseconds 1200
        } elseif ($choice -eq "2") {
            $sampleValues = @(10, 20, 30)
            foreach ($sVal in $sampleValues) {
                if ($script:StackItems.Count -lt $script:StackCapacity) {
                    $topIdx = $script:StackItems.Count
                    $addr = "0x" + ($script:StackBaseAddr + $topIdx * 4).ToString("X6")
                    $script:StackItems.Add([PSCustomObject]@{ Value = $sVal.ToString(); Address = $addr })
                }
            }
            Play-Beep "success"
            Write-Host "`n  [SUCCESS] 3 Sample elements [10, 20, 30] added! Ab aap Pop() test kar sakte hain." -ForegroundColor Green
            Start-Sleep -Milliseconds 1200
        }
        return
    }

    # When elements exist in stack:
    $lastIdx = $script:StackItems.Count - 1
    $targetItem = $script:StackItems[$lastIdx]

    Write-Host "`n  Current TOP details before POP:" -ForegroundColor Cyan
    Write-Host "  * Index          : [$lastIdx]" -ForegroundColor Yellow
    Write-Host "  * Value to POP   : '$($targetItem.Value)'" -ForegroundColor White -NoNewline
    Write-Host " (Memory Address: $($targetItem.Address))" -ForegroundColor DarkGray
    Write-Host "  * Operation      : arr[top] will be extracted and top decremented (top--)." -ForegroundColor DarkGray
    Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray

    # Step-by-step extraction animation
    Write-Host "  Step 1: Reading element '$($targetItem.Value)' at TOP [$lastIdx]..." -ForegroundColor Cyan
    Play-Beep "peek"
    Start-Sleep -Milliseconds 300

    Write-Host "  Step 2: Decrementing TOP pointer: [$lastIdx] ---> [$($lastIdx - 1)]..." -ForegroundColor Yellow
    Start-Sleep -Milliseconds 300

    Write-Host "  Step 3: Removing element from stack memory slot..." -ForegroundColor Cyan
    $script:StackItems.RemoveAt($lastIdx)
    Play-Beep "pop"
    Start-Sleep -Milliseconds 250

    Write-Host "`n  +=========================================================================+" -ForegroundColor Green
    Write-Host ("  | [SUCCESS] POP COMPLETED: Extracted '{0}' from Stack!                     |" -f $targetItem.Value) -ForegroundColor Green
    if ($script:StackItems.Count -eq 0) {
        Write-Host "  | [STATUS]  Stack is now completely EMPTY (top = -1).                     |" -ForegroundColor Yellow
    } else {
        $newTop = $script:StackItems[$script:StackItems.Count - 1]
        Write-Host ("  | [STATUS]  New TOP is now [{0}] = '{1}' ({2})            |" -f ($script:StackItems.Count - 1), $newTop.Value, $newTop.Address) -ForegroundColor Cyan
    }
    Write-Host "  +=========================================================================+" -ForegroundColor Green

    Write-Host ""
    Read-Host "  Press Enter to return to Stack visualizer"
}

function Stack-Menu {
    while ($true) {
        Clear-ScreenHeader
        Draw-StackVisual

        Write-Host "`n  OPERATIONS:" -ForegroundColor Cyan
        Write-Host "  [1] Push(x)         [4] Fill Random"
        Write-Host "  [2] Pop()           [5] Clear Stack"
        Write-Host "  [3] Peek() / Top    [6] Change Capacity"
        Write-Host "  [0] Back to Main Menu"
        Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray
        $choice = Read-Host "  Select an option [0-6]"

        switch ($choice) {
            "1" { Perform-StackPush }
            "2" { Perform-StackPop }
            "3" {
                if ($script:StackItems.Count -eq 0) {
                    Play-Beep "error"
                    Write-Host "`n  [INFO] Stack is EMPTY! top = -1" -ForegroundColor Yellow
                } else {
                    $top = $script:StackItems[$script:StackItems.Count - 1]
                    Play-Beep "peek"
                    Write-Host "`n  [PEEK] Top Element = '$($top.Value)' at index [$($script:StackItems.Count - 1)] ($($top.Address))" -ForegroundColor Cyan
                }
                Read-Host "  Press Enter to continue"
            }
            "4" {
                $script:StackItems.Clear()
                $rndCount = Get-Random -Minimum 3 -Maximum ($script:StackCapacity + 1)
                for ($i = 0; $i -lt $rndCount; $i++) {
                    $val = (Get-Random -Minimum 10 -Maximum 99).ToString()
                    $addr = "0x" + ($script:StackBaseAddr + $i * 4).ToString("X6")
                    $script:StackItems.Add([PSCustomObject]@{ Value = $val; Address = $addr })
                }
                Play-Beep "success"
                Write-Host "`n  Stack populated with $rndCount random elements." -ForegroundColor Green
                Start-Sleep -Milliseconds 700
            }
            "5" {
                $script:StackItems.Clear()
                Play-Beep "dequeue"
                Write-Host "`n  Stack cleared!" -ForegroundColor Yellow
                Start-Sleep -Milliseconds 600
            }
            "6" {
                $newCap = Read-Host "  Enter new capacity (3 to 10)"
                [int]$parsed = 0
                if ([int]::TryParse($newCap, [ref]$parsed) -and $parsed -ge 3 -and $parsed -le 10) {
                    if ($parsed -lt $script:StackItems.Count) {
                        Play-Beep "error"
                        Write-Host "`n  Cannot reduce capacity to $parsed while stack holds $($script:StackItems.Count) items!" -ForegroundColor Red
                        Start-Sleep -Milliseconds 1200
                    } else {
                        $script:StackCapacity = $parsed
                        Play-Beep "success"
                        Write-Host "`n  Stack capacity updated to $parsed." -ForegroundColor Green
                        Start-Sleep -Milliseconds 600
                    }
                } else {
                    Write-Host "  Invalid capacity. Enter a number between 3 and 10." -ForegroundColor Red
                    Start-Sleep -Milliseconds 1000
                }
            }
            "0" { return }
        }
    }
}

# ==============================================================================
# CIRCULAR QUEUE (FIFO) FUNCTIONS
# ==============================================================================

function Draw-CircularQueueVisual {
    Write-Host "`n  --- CIRCULAR QUEUE (RING BUFFER) REPRESENTATION ---" -ForegroundColor Yellow
    Write-Host "  Count: " -NoNewline
    Write-Host "$script:CQCount / $script:CQCapacity" -ForegroundColor Cyan -NoNewline
    Write-Host " | Front: " -NoNewline
    Write-Host "$script:CQFront" -ForegroundColor Green -NoNewline
    Write-Host " | Rear: " -NoNewline
    Write-Host "$script:CQRear" -ForegroundColor Magenta -NoNewline

    if ($script:CQCount -eq 0) {
        Write-Host "  [Status: EMPTY]" -ForegroundColor DarkGray
    } elseif ($script:CQCount -eq $script:CQCapacity) {
        Write-Host "  [Status: FULL]" -ForegroundColor Red
    } else {
        Write-Host "  [Status: ACTIVE]" -ForegroundColor Green
    }

    Write-Host "`n  [LINEAR MEMORY PROJECTION]" -ForegroundColor DarkCyan
    
    # Line 1: Index tags
    Write-Host "  Index:    " -NoNewline
    for ($i = 0; $i -lt $script:CQCapacity; $i++) {
        Write-Host ("  [{0}]   " -f $i) -ForegroundColor DarkGray -NoNewline
    }
    Write-Host ""

    # Line 2: Top box border
    Write-Host "            " -NoNewline
    for ($i = 0; $i -lt $script:CQCapacity; $i++) {
        Write-Host "+-------+ " -ForegroundColor DarkGray -NoNewline
    }
    Write-Host ""

    # Line 3: Values
    Write-Host "  Array:    " -NoNewline
    for ($i = 0; $i -lt $script:CQCapacity; $i++) {
        $val = $script:CQArray[$i]
        Write-Host "| " -ForegroundColor DarkGray -NoNewline
        if ([string]::IsNullOrEmpty($val)) {
            Write-Host " ... " -ForegroundColor DarkGray -NoNewline
        } else {
            Write-Host ("{0,5}" -f $val) -ForegroundColor White -NoNewline
        }
        Write-Host " | " -ForegroundColor DarkGray -NoNewline
    }
    Write-Host ""

    # Line 4: Bottom box border
    Write-Host "            " -NoNewline
    for ($i = 0; $i -lt $script:CQCapacity; $i++) {
        Write-Host "+-------+ " -ForegroundColor DarkGray -NoNewline
    }
    Write-Host ""

    # Line 5: Pointer indicators
    Write-Host "  Pointer:  " -NoNewline
    for ($i = 0; $i -lt $script:CQCapacity; $i++) {
        $isF = ($i -eq $script:CQFront)
        $isR = ($i -eq $script:CQRear)
        if ($isF -and $isR) {
            Write-Host "  F & R   " -ForegroundColor Yellow -NoNewline
        } elseif ($isF) {
            Write-Host "  FRONT   " -ForegroundColor Green -NoNewline
        } elseif ($isR) {
            Write-Host "  REAR    " -ForegroundColor Magenta -NoNewline
        } else {
            Write-Host "          " -NoNewline
        }
    }
    Write-Host ""

    # Modulo Formula HUD
    $nextRear = if ($script:CQCount -eq 0) { 0 } else { ($script:CQRear + 1) % $script:CQCapacity }
    $nextFront = if ($script:CQCount -le 1) { -1 } else { ($script:CQFront + 1) % $script:CQCapacity }
    $isFullBool = ($script:CQCount -eq $script:CQCapacity)

    Write-Host "`n  MODULO FORMULA HUD:" -ForegroundColor DarkYellow
    Write-Host "  * Next Enqueue Index : (rear + 1) % $($script:CQCapacity) = " -NoNewline
    if ($isFullBool) {
        Write-Host "BLOCKED (OVERFLOW - QUEUE IS FULL)" -ForegroundColor Red
    } else {
        Write-Host "[$nextRear]" -ForegroundColor Green
    }

    Write-Host "  * Current Dequeue Slot: Front = " -NoNewline
    if ($script:CQCount -eq 0) {
        Write-Host "NONE (UNDERFLOW - QUEUE IS EMPTY)" -ForegroundColor Red
    } else {
        Write-Host "[$script:CQFront] ('$($script:CQArray[$script:CQFront])') -> Next Front will be [$nextFront]" -ForegroundColor Green
    }

    Write-Host "  * Full Condition Check: count == capacity -> $($script:CQCount) == $($script:CQCapacity) (" -NoNewline
    if ($isFullBool) { Write-Host "TRUE - FULL" -ForegroundColor Red -NoNewline } else { Write-Host "FALSE" -ForegroundColor Green -NoNewline }
    Write-Host ")"
}

function CircularQueue-Enqueue($val) {
    if ($script:CQCount -ge $script:CQCapacity) {
        Play-Beep "error"
        Write-Host "`n  [ERROR] QUEUE OVERFLOW! Circular Queue is full ($script:CQCapacity items)." -ForegroundColor Red
        Start-Sleep -Milliseconds 1200
        return
    }

    $prevRear = $script:CQRear
    if ($script:CQCount -eq 0) {
        $script:CQFront = 0
        $script:CQRear = 0
    } else {
        $script:CQRear = ($script:CQRear + 1) % $script:CQCapacity
    }

    $script:CQArray[$script:CQRear] = $val
    $script:CQCount++
    Play-Beep "enqueue"

    $wrapMsg = ""
    if ($prevRear -ne -1 -and $script:CQRear -lt $prevRear) {
        $wrapMsg = " [CIRCULAR WRAP-AROUND OCCURRED! Rear wrapped to 0 via formula: ($prevRear + 1) % $script:CQCapacity = 0]"
    }

    Write-Host "`n  [SUCCESS] Enqueued '$val' at index [$($script:CQRear)]. Front=$($script:CQFront), Rear=$($script:CQRear)$wrapMsg" -ForegroundColor Green
    Start-Sleep -Milliseconds 700
}

function CircularQueue-Dequeue {
    Write-Host "`n  ===========================================================================" -ForegroundColor DarkCyan
    Write-Host "               CIRCULAR QUEUE DEQUEUE() OPERATION (FIFO)" -ForegroundColor Yellow
    Write-Host "  ===========================================================================" -ForegroundColor DarkCyan

    if ($script:CQCount -eq 0) {
        Play-Beep "error"
        Write-Host "`n  [!] QUEUE UNDERFLOW ERROR: Cannot Dequeue from an Empty Queue!" -ForegroundColor Red
        Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray
        Write-Host "  * Rule       : FIFO (First-In, First-Out) require karta hai ki queue me kam se kam 1 item ho." -ForegroundColor White
        Write-Host "  * Condition  : count == 0 (F = -1, R = -1)." -ForegroundColor DarkGray
        Write-Host "  * Reason     : Dequeue hamesha FRONT element ko remove karta hai, par abhi queue EMPTY hai!" -ForegroundColor Yellow
        Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray
        Write-Host "  Kya aap abhi Circular Queue me element ENQUEUE karna chahte hain?" -ForegroundColor Cyan
        Write-Host "  [1] Enter value to ENQUEUE right now" -ForegroundColor Green
        Write-Host "  [2] Auto-fill 3 sample elements (A1, B2, C3)" -ForegroundColor Yellow
        Write-Host "  [0] Skip and return to Queue Menu" -ForegroundColor DarkGray
        Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray
        $choice = Read-Host "  Select an option [1, 2, or 0]"

        if ($choice -eq "1") {
            $val = Read-Host "  Enter value to enqueue"
            if ([string]::IsNullOrWhiteSpace($val)) { $val = "A1" }
            CircularQueue-Enqueue $val
        } elseif ($choice -eq "2") {
            foreach ($s in @("A1", "B2", "C3")) {
                if ($script:CQCount -lt $script:CQCapacity) { CircularQueue-Enqueue $s }
            }
        }
        return
    }

    $prevFront = $script:CQFront
    $val = $script:CQArray[$script:CQFront]

    Write-Host "`n  Current FRONT details before DEQUEUE:" -ForegroundColor Cyan
    Write-Host "  * Index          : [$prevFront]" -ForegroundColor Yellow
    Write-Host "  * Value to Remove: '$val'" -ForegroundColor White
    Write-Host "  * Operation      : arr[front] will be removed and front moved (front + 1) % capacity." -ForegroundColor DarkGray
    Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray

    Write-Host "  Step 1: Reading element '$val' from FRONT [$prevFront]..." -ForegroundColor Cyan
    Play-Beep "peek"
    Start-Sleep -Milliseconds 300

    $script:CQArray[$script:CQFront] = $null
    $script:CQCount--

    $isWrap = $false
    if ($script:CQCount -eq 0) {
        $script:CQFront = -1
        $script:CQRear = -1
    } else {
        $wrapTest = ($prevFront + 1) % $script:CQCapacity
        if ($wrapTest -lt $prevFront) { $isWrap = $true }
        $script:CQFront = $wrapTest
    }

    Play-Beep "dequeue"
    Start-Sleep -Milliseconds 250

    Write-Host "`n  +=========================================================================+" -ForegroundColor Green
    Write-Host ("  | [SUCCESS] DEQUEUE COMPLETED: Removed '{0}' from FRONT slot [{1}]        |" -f $val, $prevFront) -ForegroundColor Green
    if ($isWrap) {
        Write-Host "  | [WRAP]    FRONT pointer WRAPPED AROUND to [0] via Modulo Formula!       |" -ForegroundColor Magenta
    }
    if ($script:CQCount -eq 0) {
        Write-Host "  | [STATUS]  Queue is now completely EMPTY (F: -1, R: -1).                 |" -ForegroundColor Yellow
    } else {
        Write-Host ("  | [STATUS]  Remaining: {0}/{1} | Next FRONT is [{2}], REAR is [{3}]     |" -f $script:CQCount, $script:CQCapacity, $script:CQFront, $script:CQRear) -ForegroundColor Cyan
    }
    Write-Host "  +=========================================================================+" -ForegroundColor Green

    Write-Host ""
    Read-Host "  Press Enter to return to Circular Queue visualizer"
}

function CircularQueue-Menu {
    while ($true) {
        Clear-ScreenHeader
        Draw-CircularQueueVisual

        Write-Host "`n  OPERATIONS:" -ForegroundColor Cyan
        Write-Host "  [1] Enqueue(x)          [5] Auto-Wrap Showcase Demo"
        Write-Host "  [2] Dequeue()           [6] Clear Queue"
        Write-Host "  [3] Peek Front          [7] Change Capacity"
        Write-Host "  [4] Peek Rear           [0] Back to Main Menu"
        Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray
        $choice = Read-Host "  Select an option [0-7]"

        switch ($choice) {
            "1" {
                $val = Read-Host "  Enter value to enqueue"
                if ([string]::IsNullOrWhiteSpace($val)) { 
                    $val = [char](65 + (Get-Random -Minimum 0 -Maximum 26)) + (Get-Random -Minimum 1 -Maximum 9).ToString()
                }
                CircularQueue-Enqueue $val
            }
            "2" { CircularQueue-Dequeue }
            "3" {
                if ($script:CQCount -eq 0) {
                    Play-Beep "error"
                    Write-Host "`n  [INFO] Queue is EMPTY!" -ForegroundColor Yellow
                } else {
                    Play-Beep "peek"
                    Write-Host "`n  [FRONT] Value = '$($script:CQArray[$script:CQFront])' at index [$($script:CQFront)]" -ForegroundColor Cyan
                }
                Read-Host "  Press Enter to continue"
            }
            "4" {
                if ($script:CQCount -eq 0) {
                    Play-Beep "error"
                    Write-Host "`n  [INFO] Queue is EMPTY!" -ForegroundColor Yellow
                } else {
                    Play-Beep "peek"
                    Write-Host "`n  [REAR] Value = '$($script:CQArray[$script:CQRear])' at index [$($script:CQRear)]" -ForegroundColor Magenta
                }
                Read-Host "  Press Enter to continue"
            }
            "5" {
                # Automated Wrap-Around Showcase
                Write-Host "`n  --- RUNNING AUTOMATED WRAP-AROUND DEMO ---" -ForegroundColor Cyan
                $script:CQArray = [string[]]::new($script:CQCapacity)
                $script:CQFront = -1
                $script:CQRear = -1
                $script:CQCount = 0

                Write-Host "  Step 1: Enqueueing 4 items (A, B, C, D)..." -ForegroundColor Yellow
                foreach ($item in @('A', 'B', 'C', 'D')) {
                    CircularQueue-Enqueue $item
                    Clear-ScreenHeader
                    Draw-CircularQueueVisual
                    Start-Sleep -Milliseconds 400
                }

                Write-Host "`n  Step 2: Dequeueing 2 items to free slots [0] and [1] at front..." -ForegroundColor Yellow
                Start-Sleep -Milliseconds 600
                CircularQueue-Dequeue
                Clear-ScreenHeader
                Draw-CircularQueueVisual
                Start-Sleep -Milliseconds 400
                CircularQueue-Dequeue
                Clear-ScreenHeader
                Draw-CircularQueueVisual

                Write-Host "`n  Step 3: Enqueueing items until REAR wraps around to index [0]!" -ForegroundColor Cyan
                Start-Sleep -Milliseconds 700
                foreach ($item in @('E', 'F', 'WRAP_1', 'WRAP_2')) {
                    if ($script:CQCount -ge $script:CQCapacity) { break }
                    CircularQueue-Enqueue $item
                    Clear-ScreenHeader
                    Draw-CircularQueueVisual
                    Start-Sleep -Milliseconds 400
                }

                Play-Beep "success"
                Write-Host "`n  [SUCCESS] Demo Complete! Notice how index [0] was reused without memory shifting!" -ForegroundColor Green
                Read-Host "`n  Press Enter to continue"
            }
            "6" {
                $script:CQArray = [string[]]::new($script:CQCapacity)
                $script:CQFront = -1
                $script:CQRear = -1
                $script:CQCount = 0
                Play-Beep "dequeue"
                Write-Host "`n  Circular Queue reset to empty state." -ForegroundColor Yellow
                Start-Sleep -Milliseconds 600
            }
            "7" {
                if ($script:CQCount -gt 0) {
                    Play-Beep "error"
                    Write-Host "`n  Cannot change capacity while queue has elements. Clear queue first!" -ForegroundColor Red
                    Start-Sleep -Milliseconds 1200
                } else {
                    $newCap = Read-Host "  Enter new capacity (4 to 8)"
                    [int]$parsed = 0
                    if ([int]::TryParse($newCap, [ref]$parsed) -and $parsed -ge 4 -and $parsed -le 8) {
                        $script:CQCapacity = $parsed
                        $script:CQArray = [string[]]::new($script:CQCapacity)
                        Play-Beep "success"
                        Write-Host "`n  Circular Queue capacity updated to $parsed." -ForegroundColor Green
                        Start-Sleep -Milliseconds 600
                    } else {
                        Write-Host "  Invalid input. Enter a number between 4 and 8." -ForegroundColor Red
                        Start-Sleep -Milliseconds 1000
                    }
                }
            }
            "0" { return }
        }
    }
}

# ==============================================================================
# APPLICATION 1: BALANCED PARENTHESES CHECKER
# ==============================================================================

function Run-ParenthesesChecker {
    Clear-ScreenHeader
    Write-Host "`n  --- STACK APPLICATION: BALANCED PARENTHESES CHECKER ---" -ForegroundColor Yellow
    Write-Host "  Used in compilers (GCC, Clang, V8) to validate syntax bracket pairings () {} [].`n" -ForegroundColor DarkGray

    Write-Host "  Presets:" -ForegroundColor Cyan
    Write-Host "  [1] {[a + (b * c)] - d}    (Balanced)"
    Write-Host "  [2] ((a + b) * [c - d])    (Balanced)"
    Write-Host "  [3] [({)]}                 (Mismatched closing bracket)"
    Write-Host "  [4] ([{}])(                (Unmatched open bracket at EOF)"
    Write-Host "  [C] Custom expression`n"

    $pick = Read-Host "  Select preset or press Enter for custom expression"
    $expr = switch ($pick) {
        "1" { "{[a + (b * c)] - d}" }
        "2" { "((a + b) * [c - d])" }
        "3" { "[({)]}" }
        "4" { "([{}])(" }
        default { Read-Host "  Enter expression" }
    }

    if ([string]::IsNullOrWhiteSpace($expr)) { $expr = "{[()]}" }

    Write-Host "`n  Evaluating expression: " -NoNewline
    Write-Host "$expr" -ForegroundColor Cyan
    Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host ("  {0,-5} | {1,-6} | {2,-30} | {3}" -f "Pos", "Char", "Action Taken", "Stack Content") -ForegroundColor DarkCyan
    Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray

    $pStack = [System.Collections.Generic.Stack[char]]::new()
    $pairs = @{ ')' = '('; '}' = '{'; ']' = '[' }
    $isBalanced = $true
    $failReason = ""

    for ($i = 0; $i -lt $expr.Length; $i++) {
        $c = $expr[$i]
        $action = ""
        
        if ($c -eq '(' -or $c -eq '{' -or $c -eq '[') {
            $pStack.Push($c)
            $action = "Push open bracket '$c'"
            Play-Beep "push"
        } elseif ($c -eq ')' -or $c -eq '}' -or $c -eq ']') {
            if ($pStack.Count -eq 0) {
                $isBalanced = $false
                $failReason = "Unmatched closing bracket '$c' with empty stack at pos $i!"
                $action = "ERROR: Stack is empty!"
                Play-Beep "error"
                Write-Host ("  {0,-5} | {1,-6} | {2,-30} | {3}" -f $i, $c, $action, "EMPTY") -ForegroundColor Red
                break
            }
            $top = $pStack.Pop()
            if ($top -eq $pairs[$c]) {
                $action = "Popped matching '$top' for '$c'"
                Play-Beep "pop"
            } else {
                $isBalanced = $false
                $failReason = "Mismatched bracket! Expected '$($pairs[$c])', found '$top' for '$c' at pos $i!"
                $action = "ERROR: Bracket mismatch!"
                Play-Beep "error"
                Write-Host ("  {0,-5} | {1,-6} | {2,-30} | {3}" -f $i, $c, $action, "[$($pStack.ToArray() -join ' ')]") -ForegroundColor Red
                break
            }
        } else {
            $action = "Operand / Operator (Skip)"
        }

        $stackStr = if ($pStack.Count -eq 0) { "EMPTY" } else { "[" + ($pStack.ToArray() -join ' ') + "]" }
        Write-Host ("  {0,-5} | {1,-6} | {2,-30} | {3}" -f $i, $c, $action, $stackStr)
        Start-Sleep -Milliseconds 150
    }

    if ($isBalanced -and $pStack.Count -gt 0) {
        $isBalanced = $false
        $failReason = "Unmatched opening bracket '$($pStack.Peek())' remaining in stack at end of expression!"
        Play-Beep "error"
    }

    Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray
    if ($isBalanced) {
        Play-Beep "success"
        Write-Host "  [RESULT] VALID & BALANCED! All brackets correctly paired and stack is clean." -ForegroundColor Green
    } else {
        Write-Host "  [RESULT] INVALID / UNBALANCED! $failReason" -ForegroundColor Red
    }

    Write-Host ""
    Read-Host "  Press Enter to return to main menu"
}

# ==============================================================================
# APPLICATION 2: CPU ROUND-ROBIN TASK SCHEDULER
# ==============================================================================

function Run-CPUScheduler {
    Clear-ScreenHeader
    Write-Host "`n  --- CIRCULAR QUEUE APPLICATION: CPU ROUND-ROBIN SCHEDULER ---" -ForegroundColor Yellow
    Write-Host "  Operating Systems use a Circular Ready Queue to allocate CPU time slices.`n" -ForegroundColor DarkGray

    $quantum = 2
    Write-Host "  Configuration: Time Quantum = $quantum units" -ForegroundColor Cyan

    $tasks = @(
        @{ Id = "P1"; Name = "DB Sync"; Burst = 5; Remaining = 5 },
        @{ Id = "P2"; Name = "Audio Stream"; Burst = 3; Remaining = 3 },
        @{ Id = "P3"; Name = "3D Render"; Burst = 6; Remaining = 6 },
        @{ Id = "P4"; Name = "Network Ping"; Burst = 2; Remaining = 2 }
    )

    $queue = [System.Collections.Generic.Queue[hashtable]]::new()
    foreach ($t in $tasks) { $queue.Enqueue($t) }

    $time = 0
    Write-Host "`n  STARTING EXECUTION TIMELINE:" -ForegroundColor Yellow
    Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray

    while ($queue.Count -gt 0) {
        $cur = $queue.Dequeue()
        $execTime = [Math]::Min($quantum, $cur.Remaining)
        $cur.Remaining -= $execTime
        $time += $execTime

        Play-Beep "peek"
        Write-Host ("  [T={0,2}] CPU Executed [{1} ({2})] for {3} units | Remaining: {4}" -f $time, $cur.Id, $cur.Name, $execTime, $cur.Remaining) -ForegroundColor Cyan

        if ($cur.Remaining -gt 0) {
            Write-Host ("         --> Quantum expired. Re-enqueued [{0}] to back of Circular Queue!" -f $cur.Id) -ForegroundColor Magenta
            Play-Beep "enqueue"
            $queue.Enqueue($cur)
        } else {
            Write-Host ("         --> [{0}] FINISHED execution! Removed from queue." -f $cur.Id) -ForegroundColor Green
            Play-Beep "pop"
        }
        Start-Sleep -Milliseconds 600
    }

    Play-Beep "success"
    Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host ("  [T={0}] ALL PROCESSES COMPLETED! CPU is now IDLE." -f $time) -ForegroundColor Green
    Write-Host ""
    Read-Host "  Press Enter to return to main menu"
}

# ==============================================================================
# ALGORITHM & CODE EXPLORER
# ==============================================================================

function Show-CodeExplorer {
    Clear-ScreenHeader
    Write-Host "`n  --- ALGORITHM COMPLEXITY & IMPLEMENTATIONS ---" -ForegroundColor Yellow
    Write-Host "`n  TIME & SPACE COMPLEXITY COMPARISON:" -ForegroundColor Cyan
    Write-Host "  +-----------------------+------------+------------+-----------------------+" -ForegroundColor DarkGray
    Write-Host "  | Data Structure / Op   | Time (Avg) | Time (Wst) | Auxiliary Space       |" -ForegroundColor White
    Write-Host "  +-----------------------+------------+------------+-----------------------+" -ForegroundColor DarkGray
    Write-Host "  | Stack: Push / Pop     |    O(1)    |    O(1)    | O(N) Array Allocation |" -ForegroundColor Green
    Write-Host "  | Stack: Peek           |    O(1)    |    O(1)    | O(1) Constant         |" -ForegroundColor Green
    Write-Host "  | Linear Queue: Dequeue |    O(1)    | O(N) shift | Memory Wasted         |" -ForegroundColor Red
    Write-Host "  | Circular Queue: Enq   |    O(1)    |    O(1)    | O(N) Ring Buffer      |" -ForegroundColor Green
    Write-Host "  | Circular Queue: Deq   |    O(1)    |    O(1)    | 100% Space Reused     |" -ForegroundColor Green
    Write-Host "  +-----------------------+------------+------------+-----------------------+" -ForegroundColor DarkGray

    Write-Host "`n  Select Code Implementation to inspect:" -ForegroundColor Cyan
    Write-Host "  [1] C++ Stack Implementation"
    Write-Host "  [2] C++ Circular Queue Implementation"
    Write-Host "  [3] Python Circular Queue Implementation"
    Write-Host "  [0] Back"
    $c = Read-Host "  Choice [0-3]"

    Clear-ScreenHeader
    switch ($c) {
        "1" {
            Write-Host "`n  C++ ARRAY-BASED STACK IMPLEMENTATION:" -ForegroundColor Yellow
            Write-Host @"
class Stack {
    int top, capacity, *arr;
public:
    Stack(int cap) {
        capacity = cap;
        arr = new int[capacity];
        top = -1;
    }
    bool isFull()  { return top == capacity - 1; }
    bool isEmpty() { return top == -1; }

    void push(int x) {
        if (isFull()) { cout << "Stack Overflow!\n"; return; }
        arr[++top] = x;
    }
    int pop() {
        if (isEmpty()) { cout << "Stack Underflow!\n"; return -1; }
        return arr[top--];
    }
    int peek() {
        return isEmpty() ? -1 : arr[top];
    }
};
"@ -ForegroundColor White
        }
        "2" {
            Write-Host "`n  C++ CIRCULAR QUEUE (RING BUFFER) IMPLEMENTATION:" -ForegroundColor Yellow
            Write-Host @"
class CircularQueue {
    int front, rear, size, capacity, *arr;
public:
    CircularQueue(int cap) {
        capacity = cap;
        arr = new int[capacity];
        front = -1; rear = -1; size = 0;
    }
    bool isFull()  { return size == capacity; }
    bool isEmpty() { return size == 0; }

    void enqueue(int val) {
        if (isFull()) return;
        if (isEmpty()) front = 0;
        rear = (rear + 1) % capacity;
        arr[rear] = val;
        size++;
    }
    int dequeue() {
        if (isEmpty()) return -1;
        int val = arr[front];
        if (front == rear) { front = -1; rear = -1; }
        else front = (front + 1) % capacity;
        size--;
        return val;
    }
};
"@ -ForegroundColor White
        }
        "3" {
            Write-Host "`n  PYTHON CIRCULAR QUEUE IMPLEMENTATION:" -ForegroundColor Yellow
            Write-Host @"
class CircularQueue:
    def __init__(self, k: int):
        self.capacity = k
        self.arr = [None] * k
        self.front = -1
        self.rear = -1
        self.size = 0

    def enqueue(self, val) -> bool:
        if self.size == self.capacity:
            return False
        if self.size == 0:
            self.front = 0
        self.rear = (self.rear + 1) % self.capacity
        self.arr[self.rear] = val
        self.size += 1
        return True

    def dequeue(self):
        if self.size == 0:
            return None
        val = self.arr[self.front]
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return val
"@ -ForegroundColor White
        }
    }
    Write-Host ""
    Read-Host "  Press Enter to return to main menu"
}

# ==============================================================================
# CONCEPT MASTERY QUIZ
# ==============================================================================

function Run-Quiz {
    Clear-ScreenHeader
    Write-Host "`n  --- DATA STRUCTURES CONCEPT QUIZ ---`n" -ForegroundColor Yellow

    $questions = @(
        @{
            Q = "What fundamental rule governs a Stack?"
            Options = @("FIFO (First In First Out)", "LIFO (Last In First Out)", "Random Access", "Priority Based")
            Correct = 2
            Expl = "Stack operates strictly on LIFO (Last In, First Out)."
        },
        @{
            Q = "In a Circular Queue of size N, what formula finds the next position of the REAR pointer?"
            Options = @("(rear + 1)", "(rear - 1) % N", "(rear + 1) % N", "(rear * 2) % N")
            Correct = 3
            Expl = "(rear + 1) % N wraps around to 0 when rear reaches N - 1."
        },
        @{
            Q = "What major flaw of a linear array queue does a Circular Queue solve?"
            Options = @("Slow O(N) access", "Memory wastage at front slots after dequeuing", "Can only store integers", "High cache misses")
            Correct = 2
            Expl = "Circular Queue reuses freed front slots without needing O(N) shifting!"
        }
    )

    $score = 0
    foreach ($i in 0..($questions.Count - 1)) {
        $q = $questions[$i]
        Write-Host "  Question $($i + 1) of $($questions.Count):" -ForegroundColor Cyan
        Write-Host "  $($q.Q)`n" -ForegroundColor White
        for ($optIdx = 0; $optIdx -lt $q.Options.Count; $optIdx++) {
            Write-Host ("  [{0}] {1}" -f ($optIdx + 1), $q.Options[$optIdx])
        }
        $ans = Read-Host "`n  Your answer (1-4)"
        [int]$parsedAns = 0
        [int]::TryParse($ans, [ref]$parsedAns) | Out-Null

        if ($parsedAns -eq $q.Correct) {
            Play-Beep "success"
            Write-Host "  --> CORRECT! $($q.Expl)`n" -ForegroundColor Green
            $score++
        } else {
            Play-Beep "error"
            Write-Host "  --> INCORRECT! Correct answer was [$($q.Correct)]. $($q.Expl)`n" -ForegroundColor Red
        }
        Start-Sleep -Milliseconds 800
    }

    Write-Host "  =================================================" -ForegroundColor DarkCyan
    Write-Host ("  FINAL SCORE: {0} / {1} ({2}%)" -f $score, $questions.Count, [Math]::Round(($score/$questions.Count)*100)) -ForegroundColor Yellow
    Write-Host "  =================================================" -ForegroundColor DarkCyan
    Read-Host "`n  Press Enter to return to main menu"
}

# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

Show-HackerIntro

while ($true) {
    Clear-ScreenHeader
    Write-Host "`n  MAIN MENU:" -ForegroundColor Yellow
    Write-Host "  [1] Stack (LIFO) Operations Lab" -ForegroundColor White
    Write-Host "  [2] Circular Queue (FIFO Ring Buffer) Lab" -ForegroundColor White
    Write-Host "  [3] Balanced Parentheses Checker (Stack Real-World App)" -ForegroundColor White
    Write-Host "  [4] CPU Round-Robin Task Scheduler (Circular Queue App)" -ForegroundColor White
    Write-Host "  [5] Algorithm Complexity & Code Explorer" -ForegroundColor White
    Write-Host "  [6] Interactive Quiz Challenge" -ForegroundColor White
    Write-Host "  [7] ⚡ Developer Intro (SWAYAM BAJPAI)" -ForegroundColor Green
    Write-Host "  [0] Exit" -ForegroundColor DarkGray
    Write-Host "  ---------------------------------------------------------------------------" -ForegroundColor DarkGreen
    $mainChoice = Read-Host "  Enter choice [0-7]"

    switch ($mainChoice) {
        "1" { Stack-Menu }
        "2" { CircularQueue-Menu }
        "3" { Run-ParenthesesChecker }
        "4" { Run-CPUScheduler }
        "5" { Show-CodeExplorer }
        "6" { Run-Quiz }
        "7" { 
            Show-HackerIntro
            Read-Host "  Press Enter to return to Main Menu"
        }
        "0" { 
            Write-Host "`n  [+] SYSTEM SHUTDOWN: Thank you for using StructLab CLI by SWAYAM BAJPAI!`n" -ForegroundColor Green
            Play-Beep "hacker"
            exit 
        }
    }
}
